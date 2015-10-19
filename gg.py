from lxml import etree
from lxml import objectify

xsd = open("extension_CCR.xsd")
genogram = open("HC.xml").read()

schema = etree.XMLSchema(file=xsd)
prsr = objectify.makeparser(schema = schema)
xmlParsed = objectify.fromstring(genogram, prsr)

print xmlParsed.Body.HealthStatusActor.DateTime.Age.Value