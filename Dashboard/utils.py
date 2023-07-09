import imgkit
from django.templatetags.static import static
from django.conf import settings
import os

def create_pastquestion_thumbnail(course_name, course_code, lecturer_name, session, pq_type, thumbnail_name):
    # print(os.getcwd())
    try:
        html_code = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <!-- <link rel="stylesheet" href="text.css"> -->
                    </head>
                    <body>
                    <div class="paper">
                        <div class="paper-lines">
                        <div class="dynamic-text">{course_name} by {lecturer_name}</div>
                        <p><B>{course_code}</B></p>
                        <p>{pq_type} {session}</p>
                        </div>
                    </div>
                    </body>
                    </html>"""

        options = {
            'format': 'png',
            'width': 150,
        }
        css = os.path.join(settings.BASE_DIR, 'static/assets/css/thumbnail.css')
        # Define the output file path
        output_path = os.path.join(settings.BASE_DIR, f'media/resources/images/{thumbnail_name}.png')
        imgkit.from_string(html_code, output_path, options=options, css=css)
        return output_path
    except Exception as e:
        print(e)