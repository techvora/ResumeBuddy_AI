import PyPDF2
import docx
from fpdf import FPDF


# CREATE FUNCTION TO TAKE OUT RAW TEXT OF RESUME FROM PDF/DOC/DOCX
def resume_text_from_pdf(pdf_file):
    if pdf_file != None:
        try:
            if pdf_file.type == 'application/pdf':

                # EXTRACT TEXT FROM PDF
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text

            elif pdf_file.type.startswith('application/vnd.openxmlformats-officedocument.wordprocessingml'):

                # # EXTRACT TEXT FROM DOC, DOCX
                doc = docx.Document(pdf_file)
                text = ""
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
                return text

            else:
                print(f"Error: Unsupported file type: {pdf_file}")
                return None

        except Exception as e:
            print(f"An error occurred while extracting text: {e}")
            return None


# CREATE FUNCTION TO DESIGN PDF
def add_line(pdf, y_axis):
    pdf.set_line_width(width=1.0)
    pdf.set_draw_color(r=255, g=179, b=40)
    pdf.line(x1=8.0, y1=y_axis, x2=202, y2=y_axis)

    # pdf.set_line_width(width=1.5)
    # pdf.set_draw_color(r=231, g=149, b=20)
    # pdf.line(x1=8.0, y1=y_axis + 1.0, x2=202, y2=y_axis + 1.0)


# PDF HEADER AND FOOTER SET
class PDFResume(FPDF):
    def __init__(self, name, position,type,left_margin=10, top_margin=15, right_margin=10,bottom_margin=22):
        super().__init__()
        self.name = name
        self.position = position
        self.type = type
        self.set_margins(left_margin, top_margin, right_margin)
        self.set_auto_page_break(auto=True, margin=bottom_margin)

    def header(self):
        """Header for each page"""
        self.set_font("Arial", "B", 14)
        self.set_text_color(r=0, g=0, b=0)
        self.text(x=10.0, y=16.5, txt=f"{self.name}")
        self.set_font("Arial", "", 12)
        self.text(x=10.0, y=24.5, txt=f"{self.position}")

        # Add logo
        if self.type == "Agency" :
            self.image("images/Inexture_logo_2023.png", x=140.0, y=14.0, w=60, h=10)

        # Add header line
        add_line(self, 28.5)

        self.set_x(10.0)
        self.set_y(33.0)

    def footer(self):
        """Footer for each page"""
        # Position at 2 cm from the bottom
        self.set_y(-15)
        add_line(self, self.get_y())
        # Set font for footer
        self.set_font("Arial", "", 12)
        # Add the footer link aligned to the left side
        if self.type == "Agency" :
            self.set_y(-12)
            self.cell(0, 10, "www.inexture.com", 0, 0, "R")


# FUNCTION TO GENERATE FREELANCE PDF FROM LLM RESPONSE
def create_resume_pdf(type,pdf_data):

    name = pdf_data["personal_details"].get("name")
    position = pdf_data["personal_details"].get("position")

    # Create the PDF object with header details
    pdf = PDFResume(name, position,type)
    pdf.add_page()

    # pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)  # Add DejaVuSans font
    # pdf.set_font("DejaVu", '', 12)

    # Define a function for multi-cell display
    def add_multi_cell(pdf, text, w, h):
        pdf.multi_cell(w=w, h=h, txt=text)
        y = pdf.get_y()

        return y

    def ensure_space_for_bullet(pdf, bullet_height, text_height):
        """
        Ensure there's enough space for both bullet and its associated text on the current page.
        If not, add a new page.
        """
        page_height = pdf.h  # Total page height
        bottom_margin = 20  # The bottom margin
        current_y = pdf.get_y()  # Current Y position

        # If the current Y position + bullet height + text height exceeds the page height, add a new page
        if current_y + bullet_height + text_height > page_height - bottom_margin:
            pdf.add_page()  # Trigger page break if not enough space

    # Introduction Section
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(r=128, g=128, b=128)
    add_multi_cell(pdf, "Introduction", w=0, h=10)
    pdf.set_text_color(r=0, g=0, b=0)

    current_y = pdf.get_y()
    # pdf.set_draw_color(r=128, g=128, b=128)
    add_line(pdf, current_y)
    # pdf.line(x1=8.0, y1=current_y + 1.0, x2=202, y2=current_y + 1.0)
    pdf.set_y(current_y + 5.0)

    pdf.set_font("Arial", '', 11)
    add_multi_cell(pdf, pdf_data["introduction"], w=0, h=7)

    current_y = pdf.get_y()
    pdf.set_y(current_y + 5.0)

    # Summary Section
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(r=128, g=128, b=128)
    add_multi_cell(pdf, "Professional Summary", w=0, h=10)
    pdf.set_text_color(r=0, g=0, b=0)

    current_y = pdf.get_y()
    # pdf.set_draw_color(r=128, g=128, b=128)
    add_line(pdf,current_y)
    # pdf.line(x1=8.0, y1=current_y + 1.0, x2=202, y2=current_y + 1.0)
    pdf.set_y(current_y + 5.0)

    pdf.set_font("Arial", '', 11)
    # add_multi_cell(pdf, pdf_data["summary"], w=0, h=8)
    for summary_points in pdf_data["summary"]:
        current_y = pdf.get_y()
        # Draw a bullet point (small filled circle)
        bullet_radius = 1  # Radius of the bullet point
        bullet_x = pdf.get_x()  # X position for bullet
        bullet_y = current_y + 3  # Center it vertically

        # Draw the bullet point
        pdf.set_fill_color(0, 0, 0)  # Set fill color to black
        pdf.ellipse(bullet_x, bullet_y, bullet_radius * 2, bullet_radius * 2, 'F')  # 'F' means fill

        # Move to the right of the bullet
        pdf.set_x(bullet_x + bullet_radius * 2 + 2)
        add_multi_cell(pdf, summary_points, w=0, h=7)
        pdf.set_x(bullet_x)

    pdf.add_page()
    # current_y = pdf.get_y()
    # pdf.set_y(current_y + 5.0)

    # Technical Skills Section
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(r=128, g=128, b=128)
    add_multi_cell(pdf, "Technical Skills", w=0, h=10)
    pdf.set_text_color(r=0, g=0, b=0)

    current_y = pdf.get_y()
    # pdf.set_draw_color(r=128, g=128, b=128)
    add_line(pdf, current_y)
    # pdf.line(x1=8.0, y1=current_y + 1.0, x2=202, y2=current_y + 1.0)
    pdf.set_y(current_y + 5.0)

    # Adding Technical Skills
    pdf.set_font("Arial", 'B', 11)  # Set font style for technical skills
    for key, value in pdf_data["technical_skills"].items():
        if value:
            # Determine how to format the key
            key_str = f"{key}:" if key == "IDEs" else f"{key.replace('_', ' ').capitalize()}: "

            current_y = pdf.get_y()
            # Draw a bullet point (small filled circle)
            bullet_radius = 1  # Radius of the bullet point
            bullet_x = pdf.get_x()  # X position for bullet
            bullet_y = current_y + 1  # Center it vertically

            # Draw the bullet point
            pdf.set_fill_color(0, 0, 0)  # Set fill color to black
            pdf.ellipse(bullet_x, bullet_y, bullet_radius * 2, bullet_radius * 2, 'F')  # 'F' means fill

            # Move to the right of the bullet
            pdf.set_x(bullet_x + bullet_radius * 2 + 2)

            # Set the font for the key (bold)
            pdf.set_font("Arial", 'B', 11)

            # Add the key as a cell (with fixed width)
            key_width = pdf.get_string_width(key_str) + 1  # Adding some padding
            pdf.cell(key_width, 6, key_str, ln=0)  # ln=0 means do not go to the next line

            # Set the font back to normal for the value
            pdf.set_font("Arial", '', 11)

            # Prepare the list string (as a comma-separated string)
            if isinstance(value, list):
                list_str = ', '.join(value)
            else:
                list_str = str(value)

            # Add the list string as a cell (allow it to wrap if necessary)
            pdf.multi_cell(0, 6, list_str)  # 0 width means it will take the remaining width

            # Optionally add a line break after each entry
            pdf.ln(5)  # Space between entries for better readability

    pdf.ln(5)  # Add some spacing before projects

    # pdf.add_page()

    # Projects Section
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(r=128, g=128, b=128)
    add_multi_cell(pdf, "Live Projects", w=0, h=10)
    pdf.set_text_color(r=0, g=0, b=0)

    current_y = pdf.get_y()
    # pdf.set_draw_color(r=128, g=128, b=128)
    add_line(pdf, current_y)
    # pdf.line(x1=8.0, y1=current_y + 1.0, x2=202, y2=current_y + 1.0)
    pdf.set_y(current_y + 5.0)

    # Add each project to the PDF
    for project, details in pdf_data["projects"].items():
        pdf.set_font("Arial", 'B', 13)
        pdf.set_text_color(r=128, g=128, b=128)
        add_multi_cell(pdf, project.upper(), w=0, h=8)
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(r=0, g=0, b=0)

        current_y = pdf.get_y()
        pdf.set_y(current_y + 3.0)

        # Timeline
        # add_multi_cell(pdf, f"Timeline: {details['timeline']}", w=0, h=10)

        # Description
        description_length = len(details["description"])
        if description_length > 15 :
            pdf.set_font("Arial", 'B', 11)
            add_multi_cell(pdf, "Description:", w=0, h=8)

            pdf.set_font("Arial", '', 11)
            add_multi_cell(pdf, details["description"], w=0, h=7)
        # pdf.set_font("Arial", 'B', 11)
        # pdf.cell(25, 8, "Description:", 0, 0)  # Fixed width for label
        # pdf.set_font("Arial", '', 11)
        # pdf.multi_cell(0, 8, details["description"])

            current_y = pdf.get_y()
            pdf.set_y(current_y + 3.0)



        # Responsibilities
        if isinstance(details["responsibilities"],list)  and (len(details["responsibilities"][0]) > 15) :
            pdf.set_font("Arial", 'B', 11)
            add_multi_cell(pdf, "Responsibilities:", w=0, h=8)
            initial_x = pdf.get_x() + 8
            pdf.set_font("Arial", '', 11)
            for responsibility in details["responsibilities"]:

                current_y = pdf.get_y()
                # Draw a bullet point (small filled circle)
                bullet_radius = 1  # Radius of the bullet point
                bullet_x = initial_x  # X position for bullet
                bullet_y = current_y + 3  # Center it vertically

                bullet_height = bullet_radius * 2
                text_height = pdf.get_string_width(responsibility) / pdf.w * 7

                # Ensure there is space for both bullet and text
                ensure_space_for_bullet(pdf, bullet_height, text_height)

                # Draw the bullet point
                pdf.set_fill_color(0, 0, 0)  # Set fill color to black
                pdf.ellipse(bullet_x, bullet_y, bullet_radius * 2, bullet_radius * 2, 'F')  # 'F' means fill

                # Move to the right of the bullet
                pdf.set_x(bullet_x + bullet_radius * 2 + 2)
                add_multi_cell(pdf, responsibility, w=0, h=7)
                pdf.set_x(initial_x)

            pdf.ln(5)

        # Skills
        # current_x = pdf.get_x()
        # pdf.set_x(current_x )
        pdf.set_font("Arial", 'B', 11)
        add_multi_cell(pdf, "Skills: " + ", ".join(details["skills"]), w=0, h=7)
        pdf.ln(7)  # Space between projects
        pdf.set_font("Arial", '', 11)


        # # Education Section
        # pdf.set_font("Arial", 'B', 14)
        # pdf.set_text_color(r=255, g=165, b=0)
        # add_multi_cell(pdf, "Education", w=0, h=10)
        # pdf.set_text_color(r=0, g=0, b=0)
        #
        # current_y = pdf.get_y()
        # # pdf.set_draw_color(r=128, g=128, b=128)
        # add_line(pdf, current_y)
        # # pdf.line(x1=8.0, y1=current_y + 1.0, x2=202, y2=current_y + 1.0)
        # pdf.set_y(current_y + 5.0)
        #
        # for university, details in pdf_data["education"].items():
        #     # Add university name
        #     pdf.set_font("Arial", 'B', 12)
        #     add_multi_cell(pdf, university, w=0, h=10)
        #
        #     # Add passing year and grade details
        #     pdf.set_font("Arial", '', 12)  # Regular font for details
        #     passing_year = details[0]  # Assuming passing year is the first element
        #     grade = details[1]  # Assuming grade is the second element
        #
        #     # Display the details (right-aligned)
        #     pdf.cell(0, 10, f"Passing Year: {passing_year}", 0, 1, "R")
        #     pdf.cell(0, 10, f"Grade: {grade}", 0, 1, "R")

            # education details
            # for grads_year in institute["responsibilities"]:
            #     add_multi_cell(pdf, "- " + responsibility, w=0, h=10)

    # Return the PDF as a string
    return pdf.output(dest='S')
