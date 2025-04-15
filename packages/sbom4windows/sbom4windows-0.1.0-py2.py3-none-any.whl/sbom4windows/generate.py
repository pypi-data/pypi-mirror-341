import sys
from pathlib import Path
import extract
import shutil

directory_location = sys.argv[1]
print (f"Processing {directory_location}")

# Check directory exists
file_dir = Path(directory_location)
if not file_dir.exists():
    print("[ERROR] Directory not found.")
    exit(-1)

temp_cab_dir = ".cab_dump"
temp_msi_dir = ".msi_dump"

DLLlist = []

for item in file_dir.glob("**/*"):
    # print (item)
    if str(item).endswith(".msi"):
        files = extract.extract_file_msi(item, temp_msi_dir)
        if files is not None:
            # Now process files
            for file in Path(temp_msi_dir).glob("**/*"):
                # print (f"Process {file}")
                if str(file).endswith(".cab"):
                    # print (f"Process {file}")
                    Path(temp_cab_dir).mkdir(parents=True, exist_ok=True)
                    # print (f"Extract to {temp_cab_dir}")
                    extract.extract_file_cab(file, temp_cab_dir)
                    # Now process extracted files
                    for cab_item in Path(temp_cab_dir).glob("**/*"):
                        if str(cab_item).endswith(".dll"):
                            # Process DLL
                            #print (f"Process {cab_item}")
                            info = extract.extract_file_dll(cab_item)
                            # print (info)
                            if len(info) > 0:
                                component_details = extract.process_dll(info)
                                # print (component_details)
                                DLLlist.append([str(item.name), str(file.name), str(cab_item.name), component_details])
                                #os.removedirs(temp_msi_dir)
                        elif str(cab_item).endswith(".cab"):
                            print(f"[CAB] Need to process {str(cab_item)}")
                        else:
                            print(f"[CAB] Not processing {str(cab_item)}")
                    shutil.rmtree(temp_cab_dir, ignore_errors=True)
                else:
                    print (f"[MSI] Not processing {file}")
            shutil.rmtree(temp_msi_dir, ignore_errors=True)
    elif str(item).endswith(".cab"):
        # print (f"Process {file}")
        Path(temp_cab_dir).mkdir(parents=True, exist_ok=True)
        # print (f"Extract to {temp_cab_dir}")
        extract.extract_file_cab(item, temp_cab_dir)
        # Now process extracted files
        for cab_item in Path(temp_cab_dir).glob("**/*"):
            if str(cab_item).endswith(".dll"):
                # Process DLL
                #print (f"Process {cab_item}")
                info = extract.extract_file_dll(cab_item)
                # print (info)
                if len(info) > 0:
                    component_details = extract.process_dll(info)
                    # print (component_details)
                    DLLlist.append([str(item.name), str(cab_item.name), "", component_details])
                    #os.removedirs(temp_msi_dir)
        shutil.rmtree(temp_cab_dir, ignore_errors=True)
    elif str(item).endswith(".dll"):
        # Process DLL
        #print (f"Process {cab_item}")
        info = extract.extract_file_dll(item)
        # print (info)
        if len(info) > 0:
            component_details = extract.process_dll(info)
            # print (component_details)
            DLLlist.append([str(item.name), "", "", component_details])
            #os.removedirs(temp_msi_dir)
    else:
        print(f"Not processing {str(item)}")

# for d in DLLlist:
#     print (d)

from lib4sbom.data.document import SBOMDocument
from lib4sbom.data.package import SBOMPackage
from lib4sbom.generator import SBOMGenerator
from lib4sbom.output import SBOMOutput
from lib4sbom.data.relationship import SBOMRelationship
from lib4sbom.sbom import SBOM

sbom_relationship = SBOMRelationship()
relationships = []
my_package = SBOMPackage()
sbom_packages = {}
application = "windows-installation"
application_id = "CDXRef-DOCUMENT"
sbom_relationship.initialise()
sbom_relationship.set_relationship(application_id, "DESCRIBES", application)
sbom_relationship.set_relationship_id(None, application_id)
relationships.append(sbom_relationship.get_relationship())
# Create packages
component_ids = {}
for d in DLLlist:
    component = d[3]
    if "name" in component:
        # Add relationships
        if d[1] != "":
            if component_ids.get((d[0].lower(), "NOTKNOWN")) is None:
                my_package.initialise()
                my_package.set_type("file")
                my_package.set_name(d[0].lower())
                my_package.set_version("NOTKNOWN")
                my_package.set_licensedeclared("NOTKNOWN")
                sbom_packages[
                    (my_package.get_name(), my_package.get_value("version"))
                ] = my_package.get_package()
                d0_id = my_package.get_value("id")
                component_ids[(d[0].lower(), "NOTKNOWN")] = d0_id
            else:
                d0_id = component_ids.get((d[0], "NOTKNOWN"))
            sbom_relationship.initialise()
            sbom_relationship.set_relationship(
                application, "DEPENDS_ON", my_package.get_value("name")
            )
            sbom_relationship.set_relationship_id(application_id, d0_id)
            relationships.append(sbom_relationship.get_relationship())
            parent = d[0].lower()
            parent_id = d0_id
        else:
            parent = application
            parent_id = application_id
        #
        if d[1] != "":
            if component_ids.get((d[1].lower(), "NOTKNOWN")) is None:
                my_package.initialise()
                my_package.set_type("file")
                my_package.set_name(d[1].lower())
                my_package.set_version("NOTKNOWN")
                my_package.set_licensedeclared("NOTKNOWN")
                sbom_packages[
                    (my_package.get_name(), my_package.get_value("version"))
                ] = my_package.get_package()
                d1_id = my_package.get_value("id")
                component_ids[(d[1].lower(), "NOTKNOWN")] = d1_id
            else:
                d1_id = component_ids.get((d[1], "NOTKNOWN"))
            sbom_relationship.initialise()
            sbom_relationship.set_relationship(
                d[0], "DEPENDS_ON", my_package.get_value("name")
            )
            sbom_relationship.set_relationship_id(d0_id, d1_id)
            relationships.append(sbom_relationship.get_relationship())
            parent = d[1].lower()
            parent_id = d1_id
        #
        my_package.initialise()

        my_package.set_name(component["name"].lower())
        my_package.set_type("library")
        if "productversion" in component:
            my_package.set_version(component["productversion"])
        if "companyname" in component:
            my_package.set_supplier("organisation", component["companyname"])
        if "legalcopyright" in component:
            my_package.set_copyrighttext(component["legalcopyright"])
        if "filedescription" in component:
            my_package.set_description(component["filedescription"])
        if "cpu" in component:
            my_package.set_property("cpu", component["cpu"])
        if "created" in component:
            my_package.set_property("created", component["created"])
        my_package.set_licensedeclared("NOTKNOWN")
        #my_package.set_checksum("MD5", hex(int(component["checksum"])))
        my_package.set_evidence(d[0])
        if d[1] != "":
            my_package.set_evidence(d[1])
        if d[2] != "":
            my_package.set_evidence(d[2])
        sbom_packages[
            (my_package.get_name(), my_package.get_value("version"))
        ] = my_package.get_package()
        sbom_relationship.initialise()
        sbom_relationship.set_relationship(
            parent, "DEPENDS_ON", my_package.get_value("name")
        )
        sbom_relationship.set_relationship_id(parent_id, my_package.get_value("id"))
        relationships.append(sbom_relationship.get_relationship())
    # else:
    #     print ("Missing data")
    #     print (d)

# Generate SBOM
my_sbom = SBOM()
my_sbom.set_type(sbom_type="cyclonedx")
my_sbom.set_version("1.6")
my_doc = SBOMDocument()
my_doc.set_value("lifecycle", "build")
my_sbom.add_document(my_doc.get_document())
my_sbom.add_packages(sbom_packages)
my_sbom.add_relationships(relationships)
#
#
my_generator = SBOMGenerator(False, sbom_type="cyclonedx", format="json")
# Will be displayed on console
my_generator.generate(application, my_sbom.get_sbom(), send_to_output=False )
sbom_output = SBOMOutput(filename=sys.argv[2], output_format="json")
sbom_output.generate_output(my_generator.get_sbom())