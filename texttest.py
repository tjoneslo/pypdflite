from pypdflite.pdflite import PDFLite


Writer = PDFLite("TestText.pdf")
#Writer.setCompression(True)
Writer.setInformation(title="Testing Text")  # set optional information
Document = Writer.getDocument()
Document.addText("Testing")
Document.addNewline(4)
Document.addText("Testing Again")
Document.addNewline()
Document.addIndent()
Document.addText("This should be enough text to test going over the edge of the page, and having to wrap back around. Let's see if it works!")
normalfont = Document.getFont()
Document.addPage()
Document.setFont('helvetica', style='B', size=24)
headerfont = Document.getFont()
Document.addNewline(2)
Document.addText("1.0 Testing a Header")

Document.setFont(font=normalfont)
Document.addNewline(2)
Document.addIndent()
Document.addText("And we're back to normal after the header.")

Document.addNewline(2)
Document.setFont('helvetica', style='BUI', size=12)
Document.addText("Testing Bold Underline Italic Style")
Document.addNewline(2)
Document.setFont("helvetica", style="BUI", size=24)
Document.addText("Testing Bold Underline Italic Style Bigger")
Document.addNewline(2)
Document.setFont("helvetica", style="BUI", size=8)
Document.addText("Testing Bold Underline Italic Style Smaller")

Document.setFont(font=normalfont)
Document.addNewline(5)
Document.addText("What")
Document.addNewline(5)
Document.addText("will")
Document.addNewline(5)
Document.addText("happen")
Document.addNewline(5)
Document.addText("when")
Document.addNewline(5)
Document.addText("I")
Document.addNewline(5)
Document.addText("go")
Document.addNewline(5)
Document.addText("on")
Document.addNewline(5)
Document.addText("to")
Document.addNewline(5)
Document.addText("the")
Document.addNewline(5)
Document.addText("next")
Document.addNewline(5)
Document.addText("page?")
Document.addNewline()
Document.addText("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")
Document.addNewline(2)
Document.addText('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras et erat dolor. Nullam id aliquam neque. Vivamus nec nibh orci. Nam faucibus dignissim diam eget tempor. Aenean neque sem, euismod sit amet tellus nec, elementum varius diam. Vestibulum in ultricies enim. Fusce imperdiet tempus lacus facilisis vestibulum. Vestibulum urna magna, dignissim vel venenatis in, pulvinar ac orci. Etiam vitae tempor metus, eu tristique mauris. Donec tincidunt purus et scelerisque sagittis. Proin semper facilisis vehicula.')
Document.addText('Pellentesque rhoncus vestibulum turpis ut varius. Nunc a rutrum est. Etiam sollicitudin rhoncus nisl, quis scelerisque felis dignissim vitae. Maecenas rutrum quam at risus mattis congue. Sed hendrerit nulla ac nunc consectetur suscipit. Fusce elementum interdum nibh, et fermentum lacus egestas non. Sed consectetur mollis tortor, eu aliquam leo tristique sit amet. Etiam nec lectus magna. Nam faucibus scelerisque velit nec cursus. Ut a dolor accumsan, gravida nunc vitae, luctus quam. Vestibulum quis gravida quam. Proin feugiat urna ut rutrum facilisis. Vivamus gravida iaculis nibh at feugiat.')

Writer.close()