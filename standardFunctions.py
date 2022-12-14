import sys
import re
import uuid

## Move used functions here

# Define a new External Repository or ignore definition if the repository is already known
# theExternalRepository - the name of the external repository
def defineExternalRepository(theExternalRepository, theDescription):
    repository.setOwnSlotValue("name", theExternalRepository)
    repository.setOwnSlotValue("description", theDescription)
    return repository



class Repository():
#    slots = {}
    instances=[]
    def print (self):
        for i in self.instances:
            i.print()
    def setOwnSlotValue(self, name, content):
#        if self == content:
            print ("Setting self in slot:"+name)
#            return
#        self.slots[name]=content

repository = Repository()

class Instance():
    def __init__(self,type,id,name):
        self.type=type
        self.id=id
        self.name=name
        self.uuid=uuid.uuid4()
        self.slots = {}
    def setOwnSlotValue(self, name, value):
        self.slots[name]=value
    def print (self):
        print ("<type>:"+self.type)
        print ("<id>:"+self.id)
        print ("<name>:"+self.name)
        for i in self.slots.keys():
            slot=self.slots[i]
            print(self.slots)
            if isinstance(slot,Instance):
                print (i + ": #"+ slot.id)
            elif type(slot) == list:
                print('[')
                for j in slot:
                    if isinstance(j,Instance):
                        print (j.name + ": #"+ j.id)
                    else:
                        print (j)
                print(']')
            else:
                print (i + ":"+ slot)
        print()

class KB:
    def getSlot(self,name):
        return name
kb=KB()

def Integer(number):
    return number


# Intelligent Essential Get Instance function.
def EssentialGetInstance(theClassName, theInstanceID, theInstanceName, theExternalID, theExternalRepositoryName):
    """ Get the Essential instance from the current repository of the specified Class.
        Firstly, the repository will be searched for the specified instance ID (internal Protege name).
        If no such instance can be found, the repository is searched for an instance with the specified external
        repository instance reference.
        If no such instance can be found, the repository is searched is for instances of the Specified class that
        has a name that exactly (case and full name) matches the specified instance name.
        If no such instance can be found, a new instance with the above the parameters is created. In this case
        Protege will automatically assign a new instance ID.

        theClassName - the name of the class of the instance to find. Search is scoped by class
        theInstanceID - the internal Protege name / ID for the instance. Set to "" to bypass search by instance ID
        theInstanceName - the name of the specified instance. When an instance is found by instance ID or External
                          reference, this parameter can be used to update the name (Essential name slot) of the
                          instance.
        theExternalID - the ID that the instance has in the specified external source repository
        theExternalRepositoryName - the name of the external source repository

        returns a reference to the correct Essential Instance or None if an attempt is made to create an instance
        of an unknown class.

        20.11.2012 JWC
    """

    print ("EssentialGetInstance(",theClassName+","+ theInstanceID+","+ theInstanceName+","+ theExternalID+","+ theExternalRepositoryName+")")
    found = None

    for i in repository.instances:
        if theInstanceID!="" and i.type==theClassName and i.id==theInstanceID:
            #print ("Updated instance via instance ID, on class: " + theClassName)
            found=i
            break
        elif i.type==theClassName and i.name==theInstanceName:
            #print ("Updated instance via name ID, on class: " + theClassName)
            found=i
            break

    if found is not None:
        if theInstanceID != "":
            found.id=theInstanceID
        found.theName=theInstanceName
    else:
        print ("Created new instance: " + theClassName)
        if theInstanceID == "":
            theInstanceID = str(uuid.uuid4())
        found=Instance(theClassName,theInstanceID,theInstanceName)
        repository.instances.append(found)

    return found

# Add the slot value to the specified instance only if it's not already there.
# theInstance - the instance to which we wish to add theInstanceToAdd
# theSlotName - the name of the slot on theInstance
# theInstanceToAdd - the instance to add to theSlotName slot on theInstance
# v1.2.1: If theSlotName is a single cardinality slot, use setSlot()
# 04.10.2011 JWC - check that the slot exists first
# 31.10.2011 JWC - Guard code, Check theInstance != None
def addIfNotThere(theInstance, theSlotName, theInstanceToAdd):
    if theInstance is None:
        print ("WARNING: Attempt to use non-existent instance: " + theSlotName)
        return

    if  theSlotName not in theInstance.slots:
        print ("WARNING: Attempt to set non-existent slot: " + theSlotName)
        theInstance.slots[theSlotName]=theInstanceToAdd
    elif isinstance(theInstance.slots[theSlotName],Instance):
        print ("WARNING: Extending slot to list: " + theSlotName)
        was=theInstance.slots[theSlotName]
        theInstance.slots[theSlotName]=[was,theInstanceToAdd]
    elif type(theInstance.slots[theSlotName])==str:
        print ("WARNING: Extending slot to list: " + theSlotName)
        was=theInstance.slots[theSlotName]
        theInstance.slots[theSlotName]=[was,theInstanceToAdd]
    else:
        theInstance.slots[theSlotName].append(theInstanceToAdd)
    return

def dump_Lucid(filename):
    if filename is None:
        print ("needs argument to set output filenames, using dummy as default");
        exit
    repository.print()
    fElements = open(filename+"Lucid.csv",'w')
    fElements.write('"ID","Level","L1","L1 Name","L2","L2 Name","L3","L3 Name","L4","L4 Name"\n')

    for i in repository.instances:
        if ('business_process_id' in i.slots):
            if (type(i.slots['business_process_id'])==str):
                printRec(fElements,i.slots['business_process_id'],i.name)
            else:
                for id in i.slots['business_process_id']:
                    printRec(fElements,id,i.name)
        if ('business_capability_level' in i.slots):
            printRec2(fElements,i)
    fElements.close()

def printRec (f,id,name):
        groups = id.split('.')
        level = len(groups) if not groups[1]=="0" else 1
        l1=groups[0]
        l2=groups[1] if len(groups)>1 else ""
        l3=groups[2] if len(groups)>2 else ""
        l4=groups[3] if len(groups)>3 else ""
        l1str=l1 + " " + normalizeStr(findById(l1 + ".0").name)
        if level>1:
            l2str=l1 + "." + l2 + " " + normalizeStr(findById(l1 + "." + l2).name)
        else:
            l2str=""
        if level>2:
            print (groups)
            l3str=l1 + "." + l2 + "." + l3 + " " + normalizeStr(findById(l1 + "." + l2 + "." + l3).name)
        else:
            l3str=""
        l4str=id + " " + normalizeStr(name)

        f.write(
         "\"" + id                            + "\","+
                str(level)                    + ","+
                l1 + ",\"" + l1str            + "\","+
                l2 + ",\"" + l2str            + "\","+
                l3 + ",\"" + l3str            + "\","+
                l4 + ",\"" + l4str            +"\"\n")

def generate_id (node):
    key="supports_business_capabilities"
    if 'business_capability_index' in node.slots:
        curindex=node.slots['business_capability_index']
    else:
        return ""
    if key in node.slots:
        parent=node.slots[key]
        if type(parent)==list:
            retval=[]
            for curparent in parent:
                parid=generate_id(curparent)
                if parid!="":
                    parid=parid+"."
                retval.append(parid+curindex)
            return retval
        else:
            parid=generate_id(parent)
            if parid!="":
                parid=parid+"."
            return parid+curindex
    else:
        return ""

def printRec2 (f,node):
        name = normalizeStr(node.name)
        level = node.slots['business_capability_level']
        if 'business_capability_index' in node.slots:
            index = node.slots['business_capability_index']
        else:
            index = '0'
        id = generate_id(node)
        if type(id)==list:
            for i, curid in enumerate(id):
                f.write(
                    "\"" + curid                            + "\","+
                    node.id                       + ","+
                    level[i]                      + ","+
                    str(index)                    + ","+
                    name                          + "\n")
        else:
            f.write(
             "\"" + id                            + "\","+
                     node.id                       + ","+
                     str(level)                    + ","+
                     str(index)                    + ","+
                     name                                                    + "\n")

def normalizeStr (x):
    return str(x.encode("ascii",'ignore').decode("ascii")).replace("\"","\"\"").replace(",","\,") if x is not None else ""

def findByUUID (uuid):
    for i in repository.instances:
        if i.uuid==uuid:
            return i
    print ("cannot find uuid:"+uuid)

def findById (id):
    if id is None:
        return None
    for i in repository.instances:
        val=i.slots['business_process_id']

        if type(val)==list:
            for j in val:
                if j==id:
                    return i
        if (val==id):
            return i

def dump_Archi(filename):
    if filename is None:
        print ("needs argument to set output filenames, using dummy as default");
        exit
    repository.print()
    fElements = open(filename+"elements.csv",'w')
    fElements.write('"ID","Type","Name","Documentation","Specialization"\n')
    fElements.write("\""+str(uuid.uuid4()) + "\",\"ArchimateModel\",\""+filename+" Capability Model\",\"Generated from APQ model\",\"\"\n")

    fRelations = open(filename+"relations.csv",'w')
    fRelations.write('"ID","Type","Name","Documentation","Source","Target","Specialization"\n')

    fProperties = open(filename+"properties.csv",'w')
    fProperties.write('"ID","Key","Value"\n')
    for i in repository.instances:
        fElements.write("\""+str(i.uuid) + "\",\"Capability\",\"" + i.name.replace("\"","\"\"")+"\",\"\",\"\"\n")

        for j in i.slots.keys():
            val = i.slots[j]
            if type(val)==list:
                vals=[]
                for k in val:
                    vals.append(str(k.uuid)) if isinstance(k,Instance) else k
                fProperties.write("\""+str(i.uuid) + "\",\""+j+"\",\""+",".join(vals)+"\"\n")
            elif isinstance(val,Instance):
                fProperties.write("\""+str(i.uuid) + "\",\""+j+"\",\""+str(val.uuid)+"\"\n")
            else:
                fProperties.write("\""+str(i.uuid) + "\",\""+j+"\",\""+val+"\"\n")

        key = None
        if 'supports_business_capabilities' in i.slots.keys():
            key='supports_business_capabilities'
        elif 'bp_sub_business_processes' in i.slots.keys():
            key='bp_sub_business_processes'

        if key is not None:
            val=i.slots[key]
            if type(val)==list:
                for j in val:
                    fRelations.write ("\""+str(uuid.uuid4()) + "\",\"CompositionRelationship\",\"\",\"\",\"" + str(i.uuid) + "\",\""+ str(j.uuid)+"\",\"\"\n")
            else:
                fRelations.write ("\""+str(uuid.uuid4()) + "\",\"CompositionRelationship\",\"\",\"\",\"" + str(i.uuid) + "\",\""+ str(val.uuid)+"\",\"\"\n")
    fElements.close()
    fRelations.close()
    fProperties.close()
