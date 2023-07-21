import os
import imgkit
from django.templatetags.static import static
from django.conf import settings
from django.db.models import Model
from pdf2image import convert_from_path
from typing import List


def generate_textbook_thumbnail(file, destination):
    
    input_file = os.path.join(settings.BASE_DIR,str(file).lstrip('/'))
        
    # Convert the first page of the PDF to an image
    images = convert_from_path(input_file, first_page=1, last_page=1, size=(220, 300))

    # Save the image thumbnail
    filename = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = os.path.join(settings.BASE_DIR,destination)
    os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist
    thumbnail_path = os.path.join(output_dir, f'{filename}_thumbnail.jpg')
    print(thumbnail_path,"thumbnail-path")
    images[0].save(thumbnail_path, 'JPEG')
    return thumbnail_path,filename

def create_pastquestion_thumbnail(course_name, course_code, lecturer_name, session, pq_type, thumbnail_name):
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
            'width': 220,
            'height': 300,
        }
        css = os.path.join(settings.BASE_DIR, 'static/assets/css/thumbnail.css')
        # Define the output file path
        output_path = os.path.join(settings.BASE_DIR, f'media/resources/images/{thumbnail_name}.png')
        imgkit.from_string(html_code, output_path, options=options, css=css)
        return output_path
    except Exception as e:
        print(e)


def convert_list_to_queryset(my_list:List, Model1:Model, Model2:Model, Model3:Model):
    # Get the primary keys of the objects for each model
    model1_pks = [obj.pk for obj in my_list if isinstance(obj, Model1)]
    model2_pks = [obj.pk for obj in my_list if isinstance(obj, Model2)]
    model3_pks = [obj.pk for obj in my_list if isinstance(obj, Model3)]

    # Retrieve the objects from the database using the primary keys
    model1_queryset = Model1.objects.filter(pk__in=model1_pks)
    model2_queryset = Model2.objects.filter(pk__in=model2_pks)
    model3_queryset = Model3.objects.filter(pk__in=model3_pks)
    
    # Combine all querysets into a single queryset
    h = {model1_queryset:len(model1_queryset), model2_queryset:len(model2_queryset), model3_queryset:len(model3_queryset)}
    h = sorted(h.items(), key=lambda item: item[1], reverse=True)
    
    combined_queryset = h[0][0].union(h[1][0], h[2][0])
    return combined_queryset

