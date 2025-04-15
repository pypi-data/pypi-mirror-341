import os
import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path


def generate(invoices_path, pdfs_path, image_path, product_id, product_name,
             amount_purchased, price_per_unit, total_price):
    """
    This function converts invoice excel files into PDF invoice

    :param invoices_path:
    :param pdfs_path:
    :param image_path:
    :param product_id:
    :param product_name:
    :param amount_purchased:
    :param price_per_unit:
    :param total_price:
    :return:
    """

    filepaths = glob.glob(f"{invoices_path}/*.xlsx")

    for filepath in filepaths:

        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()

        #pdf file name is set to excel pathname
        filename = Path(filepath).stem
        invoiceNR, date = filename.split('-')

        #set pdf file title as excel number
        pdf.set_font(family='Times', size=20, style='B')
        pdf.cell(w=50, h=8, txt=f'Invoice nr.{invoiceNR}', ln=1)

        pdf.set_font(family='Times', size=18, style='B')
        pdf.cell(w=50, h=8, txt=f'Date: {date}', align='L', ln=1)

        df = pd.read_excel(filepath, sheet_name='Sheet 1')

        #header
        columns = df.columns
        columns = [item.replace('_', ' ').title() for item in columns]
        pdf.set_font(family='Times', size=10, style='B')
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=columns[0], border=1)
        pdf.cell(w=70, h=8, txt=columns[1], border=1)
        pdf.cell(w=30, h=8, txt=columns[2], border=1)
        pdf.cell(w=30, h=8, txt=columns[3], border=1)
        pdf.cell(w=30, h=8, txt=columns[4], border=1, ln=1)

        #read and add rows
        for index, row in df.iterrows():
            pdf.set_font(family='Times', size=10)
            pdf.set_text_color(80,80, 80)
            pdf.cell(w=30, h=8, txt=str(row[product_id]), border=1)
            pdf.cell(w=70, h=8, txt=str(row[product_name]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[amount_purchased]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[total_price]), border=1, ln=1)

        #add total to page
        totalSum = df[total_price].sum()
        pdf.set_font(family='Times', size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt='', border=1)
        pdf.cell(w=70, h=8, txt='', border=1)
        pdf.cell(w=30, h=8, txt='', border=1)
        pdf.cell(w=30, h=8, txt='', border=1)
        pdf.cell(w=30, h=8, txt=str(totalSum), border=1, ln=1)

        #display your total owed
        pdf.set_font(family='Times', size=10, style='B')
        pdf.cell(w=30, h=8, txt=f'The total price is:{totalSum}', ln=1)

        #add logo
        pdf.set_font(family='Times', size=14, style='B')
        pdf.cell(w=27, h=8, txt=f'PythonHow')
        pdf.image(image_path, w=10)

        if not os.path.exists(pdfs_path):
            os.makedirs(pdfs_path)
        pdf.output(f'{pdfs_path}/{filename}.pdf')





