from __future__ import print_function

import os
import requests
import pandas as pd
import xml.etree.ElementTree as xTree
import googleapiclient as gc
from httplib2 import Http
# from oauth2client import file, client, tools
import gspread_dataframe as gd
from googleapiclient.discovery import build
df1 = pd.DataFrame()
xlFile = "XML feed.xlsx"
writeExcel = pd.ExcelWriter(xlFile)

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('XML feed.json', scope)

gc = gspread.authorize(credentials)

def getXml(url = '', xmlfile = "generatedXml.xml"):
    print("Accessing Url : ",url)

    if requests.get(url) :
        print("Reading Url content")
        info = requests.get(url)
        with open(xmlfile,'wb') as f:
            f.write(info.content)
            f.close
        xtree = xTree.parse(os.path.join(os.getcwd(), xmlfile))
        root = xtree.getroot()
        if root is not None:
            df = pd.DataFrame()
            d = {}
            cols = []
            try:
                xTree.fromstring(open(xmlfile).read())
                print("XML content is clean")

            except:
                print("Warning! Url doesnot contain end tag.")
                print("Modifying Xml file with proper end tag")
                with open(xmlfile, 'w+') as f:
                    f.append("</Events>")
                    f.close()
            print("Url content saved to XML", xmlfile)

    else:
        print("Error! Could not access url:", url)



def parseXML(xmlfile = '', sheetno = 1):

    print("Started Parsing XML")
    xtree = xTree.parse(os.path.join(os.getcwd(),xmlfile))
    root = xtree.getroot()
    if root is not None:
        df = pd.DataFrame()
        d ={}
        cols = []
        if root.findall('./Event'):
            p = './Event'
        else:
            p = './Game/Markets/Event'
        print("Events to be parsed", len(root.findall(p)))
        if len(root.findall(p)) <= 2000:
            batcheSize =  len(root.findall(p))
        else:
            batcheSize = 5000

        batch = 0
        batchNo = 0
        print("Parsing in batches: Batch", batchNo, "/", len(root.findall(p))/batcheSize)

        for event in root.findall(p):
            if batch <= batcheSize:
                for child in event:
                    if child.getchildren():
                        d = {}
                        for grand in child:
                            tag = grand.tag
                            rev_grand = {(tag+"."+ k): v for k, v in grand.items()}
                            # print("grand",grand)
                            d.update(rev_grand)
                    else:
                        tag = child.tag
                        rev_child = {(tag + "." + k): v for k, v in child.items()}
                        # print("rev_child", rev_child)

                        d.update(rev_child)
                    tag = event.tag
                    rev_event = {(tag + "." + k): v for k, v in event.items()}
                    d.update(rev_event)

                df = df.append(d, ignore_index=True,  sort=True)
                batch = batch + 1

            else:
                batch = 1

                print("Saving to ", batch/batcheSize, " Google sheet")
                if sheetno == 1:
                    wb = gc.open("XML feed")
                    print("Adding LiveLines sheet ")
                    wb.add_worksheet = "LiveLines"
                    wks = gc.open("XML feed").worksheet("LiveLines")

                elif sheetno == 2:
                    wb = gc.open("XML feed")
                    print("Adding Lines sheet ")
                    wb.add_worksheet = "Lines"
                    wks = gc.open("XML feed").worksheet("Lines")
                if batchNo == 0:
                    gd.set_with_dataframe(wks, df)
                else:
                    existing = gd.get_as_dataframe(wks)
                    updated = existing.append(df,  sort=True)
                    gd.set_with_dataframe(wks, df)

                batchNo +=  1

                df.drop(df.index, inplace=True)
                print("Parsing in batches: Batch", batchNo, "/", len(root.findall(p))/batcheSize)

        else:
            print("Warning! XML file ",xmlfile, " doesnot contain any Events or huge to extract")
    if len(root.findall(p)) <= 2000:

        print("Saving to Google sheet")
        if sheetno == 1:
            wb = gc.open("XML feed")
            print("Adding LiveLines sheet ")
            wb.add_worksheet = "LiveLines"
            wks = gc.open("XML feed").worksheet("LiveLines")

        elif sheetno == 2:
            wb = gc.open("XML feed")
            print("Adding Lines sheet ")
            wb.add_worksheet = "Lines"
            wks = gc.open("XML feed").worksheet("Lines")
        dummy = pd.DataFrame()
        dummy.update({})
        gd.set_with_dataframe(wks, dummy)
        gd.set_with_dataframe(wks, df)

    return df


if __name__ == '__main__':

    while(1):

        xmlfile = 'LiveLines.xml'
        url ="http://xml.10bet.co.uk/livelines.aspx"
        getXml(url, xmlfile)
        df = parseXML(xmlfile,1)

        xmlfile = 'Lines.xml'
        url ="http://xml.10bet.co.uk/lines.aspx"
        getXml(url, xmlfile)
        df = parseXML(xmlfile,2)

