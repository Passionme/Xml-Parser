import pandas as pd
import io
import lxml.etree as ET
from lxml import etree
import xlsxwriter

COL = ["RegisteredName","ValidVotes"]
df2 = pd.DataFrame(columns = COL )
df = pd.DataFrame()
tree = ET.parse('Telling_TK2017_gemeente_Aalsmeereml.xml')
root = tree.getroot()
# content = etree.tostring(root)
# contentBuffer=io.BytesIO(content)
# context = ET.iterparse(contentBuffer,tag='Contest')
# print(tree, tree.find('Count'))
l3=[]
l4=[]
for child1 in root.iter():
    if child1.getchildren():
        for child2 in child1.iter():
            if child2.getchildren():
                for child3 in child2.iter():
                    if child3.getchildren():
                        for child4 in child3.iter():
                            if child4.text :
                                if len(l4) == 0 and not (child4.text).isalpha():
                                    pass
                                else:
                                    l4.append(child4.text)
                                    if len(l4) == 2:
                                        # print(df.append(pd.DataFrame(l4)))
                                        df = df.append(pd.DataFrame([l4],columns = COL), ignore_index = True)
                                        # print(df)
                                        l4 = []
                                # print("child4",child4.tag, child4.text)

                    else:
                        if child3.text:
                            if len(l3) == 0 and not (child3.text).isalpha():
                                pass
                            else:
                                l3.append(child3.text)
                                if len(l3) == 2:
                                    # print(pd.DataFrame(l3))
                                    df = df.append(pd.DataFrame([l3],columns = COL) ,ignore_index = True)
                                    # print(df)
                                    l3 = []
                        # print(df)

# print(df)
writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()
