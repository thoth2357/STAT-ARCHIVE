import os
import imgkit
from django.templatetags.static import static
from django.conf import settings
from django.db.models import Model
from pdf2image import convert_from_path
from typing import List
from itertools import chain
from operator import attrgetter


def generate_textbook_thumbnail(file, destination):
    input_file = os.path.join(settings.BASE_DIR, str(file).lstrip('/'))

    # Convert the first page of the PDF to an image
    images = convert_from_path(input_file, first_page=1, last_page=1, size=(220, 300))

    # Save the image thumbnail
    filename = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = os.path.join(settings.BASE_DIR, destination)
    os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist
    thumbnail_path = os.path.join(output_dir, f'{filename}_thumbnail.jpg')
    print(thumbnail_path, "thumbnail-path")
    images[0].save(thumbnail_path, 'JPEG')
    return thumbnail_path, filename


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


def convert_list_to_queryset(my_list: List, Model1: Model, Model2: Model, Model3: Model):
    # Get the primary keys of the objects for each model
    model1_pks = [obj.pk for obj in my_list if isinstance(obj, Model1)]
    model2_pks = [obj.pk for obj in my_list if isinstance(obj, Model2)]
    model3_pks = [obj.pk for obj in my_list if isinstance(obj, Model3)]

    # Retrieve the objects from the database using the primary keys
    model1_queryset = Model1.objects.filter(pk__in=model1_pks).values("id", "Name", "Type", "file", "thumbnail","Date_uploaded")
    model2_queryset = Model2.objects.filter(pk__in=model2_pks).values("id", "Name", "Type", "file", "thumbnail","Date_uploaded")
    model3_queryset = Model3.objects.filter(pk__in=model3_pks).values("id", "Name", "Type", "file", "thumbnail","Date_uploaded")

    # print(model1_queryset, "testing1\n")
    # print(model2_queryset, "testing2\n")
    # print(model3_queryset, "testing3\n")


    # # Combine all querysets into a single queryset
    h = {model1_queryset: len(model1_queryset), model2_queryset: len(model2_queryset),
         model3_queryset: len(model3_queryset)}
    h = sorted(h.items(), key=lambda item: item[1], reverse=False)

    h = [(item[0], item[1], item[0].model.__name__) for item in h]


    h = [item for item in h if item[0]]
    size = len(h)
    print("\n", h, "bastards", size)
    # # for i in h:
    # #     h[0][0].union()
    if 1 < size < 3:  # sloppy code here , fix after deadline
        combined_queryset = h[0][0].union(h[size - 1][0])
    elif size > 1 and size == 3:
        combined_queryset = h[0][0].union(h[size - 2][0], h[size - 1][0])
    else:
        combined_queryset = h[0][0]

    print("combined", combined_queryset)
    # results_list = sorted(
    #     combined_queryset,
    #     key=attrgetter('Date_uploaded')
    # )
    # print(results_list, "results list")
    v = model1_queryset.union(model2_queryset, model3_queryset)
    return combined_queryset

def unionalize_models(model1, model2,model3):
    model1_query = model1.objects.all().values("id", "Name", "Type", "file", "thumbnail")
    model2_query = model2.objects.all().values("id", "Name", "Type", "file", "thumbnail")
    model3_query = model3.objects.all().values("id", "Name", "Type", "file", "thumbnail")

    final = model1_query.union(model2_query, model3_query)
    return final


def filter_by_type(id_name_list ,model1,model2,value):
    type_model_mapping = {
        'Text_Questions': model1,
        'Exam_Questions':model1,
        'Project': model2,
        # Add more mappings for other types if needed
    }

    filtered_querysets = []
    model_objects_set = set()  # Set to store model objects that have been added

    for item in id_name_list:
        record_id, record_name, record_type = item
        model = type_model_mapping.get(record_type)
        if model is not None:
            # Filter the records based on the model
            queryset = model.objects.filter(id=record_id, Name=record_name, Session=value)
            
            # Check if the model object is not already in the set before adding it
            model_object = queryset.first()
            if model_object not in model_objects_set:
                filtered_querysets.append(queryset)
                model_objects_set.add(model_object)
                
    # Take the union of all filtered querysets
    combined_queryset = filtered_querysets[0].union(*filtered_querysets[1:])

    return combined_queryset
