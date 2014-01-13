from os.path import splitext
from pdfobjects.pdffont import PDFFont
from pdfobjects.pdfpage import PDFPage
from pdfobjects.pdfcolorscheme import PDFColorScheme
from pdfobjects.pdftext import PDFText
from pdfobjects.pdfcursor import PDFCursor
from pdfobjects.pdfline import PDFLine
from pdfobjects.pdfrectangle import PDFRectangle
from pdfobjects.pdftable import PDFTable
from pdfobjects.pdfimage import PDFImage
from pdfobjects.pdfttfonts import PDFTTFont


class PDFDocument(object):

    """ The Document object is the base class that
        is used to add and manage the content of the
        pdf file.

        Document maintains lists of pages and other
        resources, provides for default selections,
        which can be changed through the convinence
        methods.

        Note that page and text objects do not maintain
        fonts themselves. If they must use them (for
        calculating widths or such), they must have
        the current font passed to them.

    """

    def __init__(self, session, orientation, layout):
        "Sets up a standard default document."
        self.session = session
        self.pages = []
        self.fonts = []
        self.fontkeys = []               # array of used fonts

        self.images = []
        self.imagekeys = []
        self.image_filter = None

        self.orientation_default = orientation
        self.layout_default = layout

        self.diffs = []

        self._set_defaults()

    def _set_defaults(self):
        "Set color scheme & font to defaults."
        self.set_color_scheme()
        self._set_default_font()
        self.add_page()     # add first page

    def set_color_scheme(self, color_scheme=None):
        """ Default color object is black letters
            & black lines.

        """
        if color_scheme is None:
            self.color_scheme = PDFColorScheme()
        else:
            if isinstance(color_scheme, PDFColorScheme):
                self.color_scheme = color_scheme
                print self.color_scheme
            else:
                raise Exception("Color scheme not a PDFColorScheme object")

    def get_color_scheme(self):
        return self.color_scheme

    def _set_default_font(self):
        """ Internal method to set the
            initial default font. Change
            the font using set_font method.

        """
        self.font = PDFFont(self.session)
        self.font._set_index()
        self.fonts.append(self.font)
        self.fontkeys.append(self.font.font_key)

    def add_page(self, page=None):
        """ May generate and add a PDFPage
            separately, or use this to generate
            a default page.

        """
        if page is None:
            self.page = PDFPage(self.orientation_default, self.layout_default)
        else:
            self.page = page
        self.page._set_index(len(self.pages))
        self.pages.append(self.page)
        currentfont = self.font
        self.set_font(font=currentfont)

    def get_page(self):
        "Returns reference to current page object."
        return self.page

    def get_new_cursor(self):
        " Returns a new default cursor "
        return PDFCursor()

    def set_cursor(self, cursor=None, x=None, y=None):
        if cursor is not None:
            self.page.set_cursor(cursor)
        elif x is not None and y is not None:
            self.page.set_cursor(PDFCursor(x, y))


    def set_font(self, family=None, style=None, size=None, font=None, tt=False):
        """ Set the document font object, size given in points.
            If family, style, and/or size is given, generates
            a new Font object, checks to see if it is already
            in use, and selects it.

            May also use the font keyword to add an already
            instantiated PDFFont object.

        """
        if font:
            testfont = font
        else:
            # If size is not defined, keep the last size.
            if size is None:
                size = self.font.font_size

            # Create a font from givens to test its key
            if tt is False:
                testfont = PDFFont(self.session, family, style, size)
            else:
                testfont = PDFTTFont(self.session, family, style, size)

        testkey = testfont.font_key

        if testkey in self.fontkeys:
            # It's already there.
            index = self.fontkeys.index(testkey)
            self.font = self.fonts[index]
        else:
            self.font = testfont
            self._register_new_font(self.font)

        if(self.page.index > 0):
            self.session._out('BT /F%d %.2f Tf ET' %
                              (self.font.index, self.font.font_size),
                              self.page)

    def get_font(self):
        """ Get the current font object. Useful for storing
            in variables, and switching between styles.

        """
        return self.font

    def set_font_size(self, size):
        "Convinence method for just changing font size."
        if(self.font.font_size == size):
            pass
        else:
            self.set_font(self.font.family, self.font.style, size)

    def add_text(self, text, cursor=None):
        """ Input text, short or long. Writes in order, within the
            pre-defined page boundaries. Use add_newline as a return
            character. Sequential add_text commands will print without
            additional whitespace.

            Currently all "left-justified", although that may change in
            future version.

        """
        text = PDFText(self.session, self.page, self.font, self.color_scheme,
                       text, cursor)

    def add_newline(self, number=1):
        """ Starts over again at the new line. If number is specified,
            it will leave multiple lines.
        """
        if isinstance(number, int):
            try:
                self.page.add_newline(self.font, number)
            except ValueError:
                self.add_page()
        else:
            raise TypeError("Number of newlines must be an integer.")

    def add_indent(self):
        """ Adds a standard tab of 4 spaces.
        """
        self.page.add_indent(self.font)

    def add_line(self, x1=None, y1=None, x2=None, y2=None,
                 cursor1=None, cursor2=None, style="solid"):
        if cursor1 is not None:
            if cursor2 is not None:
                pass
        else:
            cursor1 = PDFCursor(x1, y1)
            cursor2 = PDFCursor(x2, y2)

        myline = PDFLine(
            self.session, self.page, self.color_scheme,
            cursor1, cursor2, style)
        myline.draw()

    def draw_horizonal_line(self):
        end_cursor = self.page.cursor.copy()
        end_cursor.x = end_cursor.xmax

        myline = PDFLine(self.session, self.page,
                         self.color_scheme, self.page.cursor, end_cursor, None)
        myline.draw()

    def draw_rectangle(self, x1=None, y1=None, x2=None, y2=None,
                       width=None, height=None, cursor1=None, cursor2=None,
                       style='S'):
        if cursor1 is not None:
            if cursor2 is not None:
                pass
            elif width is not None and height is not None:
                dims = PDFCursor(width, height)
                cursor2 = cursor1.add(dims)
            elif x2 is not None and y2 is not None:
                cursor2 = PDFCursor(x2, y2)
            else:
                raise Exception("Rectangle not defined")
        else:
            if x1 is not None and y1 is not None:
                cursor1 = PDFCursor(x1, y1)
                if x2 is not None and y2 is not None:
                    cursor2 = PDFCursor(x2, y2)
                elif width is not None and height is not None:
                    dims = PDFCursor(width, height)
                    cursor2 = cursor1.add(dims)
                else:
                    raise Exception("Rectangle not defined")
            else:
                raise Exception("Rectangle not defined")

        rectangle = PDFRectangle(
            self.session, self.page, self.color_scheme, cursor1, cursor2,
            size=1, style=style)

        rectangle.draw()

    def add_table(self, datalist, cursor=None):
        if cursor is None:
            tablecursor = self.page.cursor
        else:
            tablecursor = cursor

        table = PDFTable(self.session, self.page, datalist, self.font,
                         self.color_scheme, tablecursor)

        table.draw()
        self.page.cursor = table.cursor

    def add_image(self, image=None, name=None, cursor=None,):
        if not cursor:
            imagecursor = self.page.cursor
        else:
            imagecursor = cursor

        if isinstance(image, PDFImage):  # It's an image object
            myimage = self._get_image(image.name)
            if not myimage:
                self._register_new_image(image)
            myimage = image

        elif isinstance(image, str):  # Name or path
            image_string = image
            if image_string.find('.') == -1:  # Not a path, treat as name
                myimage = self._get_image(image_string)
                if not myimage:
                    raise Exception('Not a proper image path')
            else:  # Is a path
                if not name:  # But it doesn't have a name specified.
                    name = splitext(image_string)[0]  # Specify it
                myimage = self._get_image(name)
                if not myimage:  # New image
                    myimage = PDFImage(self.session, image_string, name,
                                       imagecursor)
                    self._register_new_image(myimage)
        myimage.draw(self.page)

        # If a cursor was not specified, place at the end
        if not cursor:
            self.page.cursor = myimage.cursor
        return myimage

    def _get_image(self, image_name):
        if image_name in self.imagekeys:
            index = self.imagekeys.index(image_name)
            myimage = self.images[index]
            return myimage
        else:
            return False

    def _output_pages(self):
        """ Called by the PDFLite object to prompt creating
            the page objects.

        """
        if self.orientation_changes is None:
            self._get_orientation_changes()
        else:
            # Page
            for page in self.pages:
                obj = self.session._add_object()
                self.session._out('<</Type /Page')
                self.session._out('/Parent 1 0 R')
                if page in self.orientation_changes:
                    self.session._out(
                        '/MediaBox [0 0 %.2f %.2f]' %
                        (page.width, page.height))
                self.session._out('/Resources 2 0 R')
                self.session._out('/Group <</Type /Group /S /Transparency /CS /DeviceRGB>>')
                self.session._out('/Contents %s 0 R>>' % (obj.id + 1))
                self.session._out('endobj')

                # Page content
                self.session._add_object()
                if self.session.compression is True:
                    textfilter = ' /Filter /FlateDecode '
                    page._compress()
                else:
                    textfilter = ''
                self.session._out('<<%s/Length %s >>' % (textfilter, len(page.buffer)))
                self.session._put_stream(page.buffer)
                self.session._out('endobj')

    def _get_orientation_changes(self):
        """ Returns a list of the pages that have
            orientation changes.

        """
        self.orientation_changes = []
        for page in self.pages:
            if page.orientation_change is True:
                self.orientation_changes.append(page.index)
            else:
                pass
        return self.orientation_changes

    def _register_new_font(self, font):
        font._set_index(len(self.fonts) + 1)
        self.fonts.append(self.font)
        self.fontkeys.append(self.font.font_key)
        if hasattr(font, 'diffs') and font.diffs is not None:
            try:
                index_of_diff = self.diffs.index(font.diffs)
            except:
                index_of_diff = len(self.diffs) + 1
                self.diffs.append(font.diffs)
            font.diff_number = index_of_diff

    def _output_fonts(self):
        """ Called by the PDFLite object to prompt creating
            the font objects.

        """
        self.session._save_object_number()
        self._output_encoding_diffs()
        self._output_font_files()

        for font in self.fonts:
            obj = self.session._add_object()
            font._set_number(obj.id)
            font.output()

    def _output_font_files(self):
        for font in self.fonts:
            if hasattr(font, 'file'):
                font.output_file()

    def _output_encoding_diffs(self):
        if self.diffs:
            for diff in self.diffs:
                obj = self.session._add_object()
                self.session._out('<</Type /Encoding /BaseEncoding /WinAnsiEncoding /Differences [%s]>>')
                self.session._out('endobj')

    def _register_new_image(self, image):
        image._set_index(len(self.images) + 1)
        self.images.append(image)
        self.imagekeys.append(image.name)

    def _output_images(self):
        """ Creates reference images, that can be
            drawn throughout the document.

        """
        for image in self.images:
            obj = self.session._add_object()
            image._set_number(obj.id)
            image.output()
