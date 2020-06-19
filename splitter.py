import io

from PyPDF2 import PdfFileReader, PdfFileWriter


def splitter(pdf_stream, split_type='horizontal'):
    ''' ファイル読み込み '''
    original_L = PdfFileReader(pdf_stream, strict=False)
    original_R = PdfFileReader(pdf_stream, strict=False)

    ''' 暗号化解除 '''
    if original_L.isEncrypted:
        original_L.decrypt('')
        original_R.decrypt('')

    marged = PdfFileWriter()
    for i in range(original_L.getNumPages()):
        ''' オリジナルページ取得 '''
        page_L = original_L.getPage(i)
        page_R = original_R.getPage(i)

        if split_type == 'horizontal':
            ''' 水平方向に分割 '''
            page_width = page_L.mediaBox.getWidth()
            page_L.mediaBox.lowerRight = (
                page_width / 2,
                page_L.mediaBox.getLowerRight_y()
            )
            page_R.mediaBox.upperLeft = (
                page_width / 2,
                page_R.mediaBox.getUpperLeft_y()
            )

        elif split_type == 'vertical':
            ''' 垂直方向に分割 '''
            page_height = page_L.mediaBox.getHeight()
            page_L.mediaBox.lowerRight = (
                page_L.mediaBox.getLowerRight_x(),
                page_height / 2
            )
            page_R.mediaBox.upperLeft = (
                page_R.mediaBox.getUpperLeft_x(),
                page_height / 2
            )

        ''' ページ追加 '''
        marged.addPage(page_L)
        marged.addPage(page_R)

    ''' 出力 '''
    output = io.BytesIO()
    marged.write(output)

    return output.getvalue()
