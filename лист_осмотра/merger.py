
def merg(a):
    merger = PdfFileMerger()

    for pdf in a:
        merger.append(pdf)

    merger.write("result.pdf")
    merger.close()
