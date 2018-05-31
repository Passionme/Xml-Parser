# import xml.etree.ElementTree as ET
import pandas as pd
import io
import lxml.etree as ET
from lxml import etree
import xlsxwriter

df = pd.DataFrame(columns=["ContectName","RegisteredName","ValidVotes"])

tree = ET.parse('Telling_TK2017_gemeente_Aalsmeereml.xml')
root = tree.getroot()
content = etree.tostring(root)
contentBuffer=io.BytesIO(content)
context = ET.iterparse(contentBuffer,tag='Contest')
for child in root.iter():
    print(tree.getpath(child))
for action, elem in context:
    print(elem.xpath('/Contest/ContestIdentifier/ContestName/text()'))
    id=elem.xpath('id')
    # RegName=elem.xpath('Selection/AffiliationIdentifier/RegisteredName/')
    # for field,value in zip(fields,values):
    #     print('\t{f} = {v}'.format(f=field,v=value))


# for child in root:
#     print("yes", child.tag,child.getchildren())
#     if ("Count" in child.tag) and  child.getchildren():
#         for subchild1 in child.iter():
#             for subchild2 in subchild1.iter():
#                 for subchild3 in subchild2.iter():
#                     df.append([subchild1,subchild2,subchild3])
#                     # print("child", child.tag,"subchild", subchild3.tag)

# print(df)
writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()
# parser = ET.XMLPullParser(['start','end'])
# for event, elem in parser.read_events():
#     print("event",event)
#     print(elem.tag)