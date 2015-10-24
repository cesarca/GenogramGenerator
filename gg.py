from lxml import etree
from lxml import objectify


class Patient:
    def __init__(self, xml):
        self.age = self.parse_patient_age(xml)
        self.hastumor = self.parse_patient_tumor_presence(xml)
        self.status = self.parse_patient_status(xml)
        self.code = self.parse_patient_code(xml)
        self.codingsystem = self.parse_patient_coding_system(xml)
        self.version = self.parse_patient_coding_system_version(xml)
        self.relatives = self.parse_patient_relatives(xml)

    def parse_patient_coding_system_version(self, xml):
        return xml.Body.HealthStatusActor.Description.Code.Version

    def parse_patient_coding_system(self, xml):
        return xml.Body.HealthStatusActor.Description.Code.CodingSystem

    def parse_patient_code(self, xml):
        return xml.Body.HealthStatusActor.Description.Code.Value

    def parse_patient_status(self, xml):
        return 'alive' if xml.Body.HealthStatusActor.Description.Text == 'Vivo' else 'dead'

    def parse_patient_tumor_presence(self, xml):
        return True if xml.Body.HealthStatusActor.PresenceOfTumor == 'Si' else False

    def parse_patient_age(self, xml):
        return xml.Body.HealthStatusActor.DateTime.Age.Value

    def parse_patient_relatives(self, xml):
        return [Relative(actor) for actor in xml.Actors.Actor]

    def __str__(self):
        print self.__dict__


class Relative:
    def __init__(self, xml):
        self.actor_object_id = self.parse_actor_object_id(xml)
        self.name_given, self.name_middle, self.name_family, self.name_display_name = self.parse_name(xml)
        self.birth_date = self.parse_birth_date(xml)
        self.gender, self.gender_code_value, gender_code_coding_system, gender_code_version = self.parse_gender(xml)
        self.relation = self.parse_relation(xml)
        self.source_description = self.parse_source_description(xml)

    def parse_source_description(self, xml):
        return xml.Source.Description.Text

    def parse_relation(self, xml):
        return xml.Relation.Text

    def parse_gender(self, xml):
        gender = xml.Person.Gender
        return gender.Text, gender.Code.Value, gender.Code.CodingSystem, gender.Code.Version

    def parse_birth_date(self, xml):
        return xml.Person.DateOfBirth.ExactDateTime

    def parse_name(self, xml):
        name = xml.Person.Name
        return name.CurrentName.Given, name.CurrentName.Middle, name.CurrentName.Family, name.DisplayName

    def parse_actor_object_id(self, xml):
        return xml.ActorObjectID

    def __str__(self):
        print self.__dict__

class XmlParser:
    _XSD_FILE = "extension_CCR.xsd"
    _CLINICAL_HISTORY_FILE = "HC.xml"

    def __init__(self):
        self.xsd = open("extension_CCR.xsd")
        self.clinical_history = open("HC.xml").read()
        self.xml_parser = self.build_xml_parser()

    def build_xml_parser(self):
        schema = etree.XMLSchema(file=self.xsd)
        return objectify.makeparser(schema=schema)

    def parse(self):
        return objectify.fromstring(self.clinical_history, self.xml_parser)


xml_parsed = XmlParser().parse()

p = Patient(xml_parsed)
p.__str__()

print p.relatives[0].__str__()