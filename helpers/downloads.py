from bclabels.models import BCLabel
from tklabels.models import TKLabel
from projects.models import ProjectContributors
from .models import Notice

from django.http import HttpResponse
from .utils import generate_zip, render_to_pdf
import requests

# Open to Collaborate Notice
def download_otc_notice():
    baseURL = 'https://storage.googleapis.com/anth-ja77-local-contexts-8985.appspot.com/'
    institution_text = "The Institution Notices are for use by collecting institutions, data repositories, researchers, and organizations who engage in collaborative curation with Indigenous and other marginalized communities who have been traditionally excluded from processes of documentation and record keeping.\nThe Institution Notices are intended to be displayed prominently on public-facing institutional websites, on digital collections pages and or in finding aids."

    # Initialize README TEXT
    readme_text = ''
    readme_text = institution_text + '\n\nThis folder contains the following files:\n'
    
    files = []

    open_to_collab_text = 'Our institution is committed to the development of new modes of collaboration, engagement, and partnership with Indigenous peoples for the care and stewardship of past and future heritage collections.'

    get_img = requests.get(baseURL + 'labels/notices/ci-open-to-collaborate.png')
    get_svg = requests.get(baseURL + 'labels/notices/ci-open-to-collaborate.svg')
    files.append(('Open_To_Collaborate' + '.png', get_img.content))
    files.append(('Open_To_Collaborate' + '.svg', get_svg.content))
    files.append(('Open_To_Collaborate' + '.txt', open_to_collab_text))

    # Create Readme
    file_names = []
    for f in files:
        file_names.append(f[0])
    readme_content = readme_text + '\n'.join(file_names) + '\n\nRefer to the Usage Guides (https://localcontexts.org/support/downloadable-resources/) for details on how to adapt and display the Open To Collaborate Notice.\n\nFor more information, contact Local Contexts at localcontexts.org or support@localcontexts.org'
    files.append(('README.txt', readme_content))

        # Generate zip file 
    full_zip_in_memory = generate_zip(files)

    zipfile_name = f"LC-Open_to_Collaborate_notice.zip"

    response = HttpResponse(full_zip_in_memory, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(zipfile_name)

    return response

# Download approved community Labels
def download_labels_zip(community):
    bclabels = BCLabel.objects.filter(community=community, is_approved=True)
    tklabels = TKLabel.objects.filter(community=community, is_approved=True)

    template_path = 'snippets/pdfs/community-labels.html'
    context = {'community': community, 'bclabels': bclabels, 'tklabels': tklabels,}

    files = []

    # Add PDF to zip
    pdf = render_to_pdf(template_path, context)
    files.append(('Labels_Overview.pdf', pdf))

    # Add Label images, text and translations
    for bclabel in bclabels:
        get_image = requests.get(bclabel.img_url)
        get_svg = requests.get(bclabel.svg_url)
        files.append((bclabel.name + '.png', get_image.content))
        files.append((bclabel.name + '.svg', get_svg.content))

        # Default Label text
        text_content = bclabel.name + '\n' + bclabel.label_text
        text_addon = []

        if bclabel.bclabel_translation.all():
            for translation in bclabel.bclabel_translation.all():
                text_addon.append('\n\n' + translation.translated_name + ' (' + translation.language + ') ' + '\n' + translation.translated_text)
            files.append((bclabel.name + '.txt', text_content + '\n'.join(text_addon)))
        else:
            files.append((bclabel.name + '.txt', text_content))

    # Add Label images, text and translations
    for tklabel in tklabels:
        get_image = requests.get(tklabel.img_url)
        get_svg = requests.get(tklabel.svg_url)
        files.append((tklabel.name + '.png', get_image.content))
        files.append((tklabel.name + '.svg', get_svg.content))
        
        # Default Label text
        text_content = tklabel.name + '\n' + tklabel.label_text
        text_addon = []

        if tklabel.tklabel_translation.all():
            for translation in tklabel.tklabel_translation.all():
                text_addon.append('\n\n' + translation.translated_name + ' (' + translation.language + ') ' + '\n' + translation.translated_text)
            files.append((tklabel.name + '.txt', text_content + '\n'.join(text_addon)))
        else:
            files.append((tklabel.name + '.txt', text_content))
    
    # Create Readme
    readme_text = "The Traditional Knowledge (TK) and Biocultural (BC) Labels reinforce the cultural authority and rights of Indigenous communities.\nThe TK and BC Labels are intended to be displayed prominently on public-facing Indigenous community, researcher and institutional websites, metadata and digital collection's pages.\n\nThis folder contains the following files:\n"
    file_names = []
    for f in files:
        file_names.append(f[0])
    readme_content = readme_text + '\n'.join(file_names) + '\n\nRefer to the Usage Guides (https://localcontexts.org/support/downloadable-resources/) for details on how to adapt and display the Labels for your community.\n\nFor more information, contact Local Contexts at localcontexts.org or support@localcontexts.org'
    files.append(('README.txt', readme_content))

    # Generate zip file 
    full_zip_in_memory = generate_zip(files)

    response = HttpResponse(full_zip_in_memory, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(community.community_name + '-Labels.zip')

    return response

# Download Project
def download_project_zip(project):
    baseURL = 'https://storage.googleapis.com/anth-ja77-local-contexts-8985.appspot.com/'
    project_bclabels = project.bc_labels.all()
    project_tklabels = project.tk_labels.all()
    project_creator = project.project_creator_project.first()
    contributors = ProjectContributors.objects.prefetch_related('communities', 'institutions', 'researchers').get(project=project)
    project_people = project.additional_contributors.all()

    notice_exists = Notice.objects.filter(project=project).exists()

    template_path = 'snippets/pdfs/project-pdf.html'
    context = { 'project': project, 'project_creator': project_creator, 'contributors': contributors, 'project_people': project_people }

    files = []

    # Initialize README TEXT
    readme_text = ''

    # Set README text if both types of notice present
    if notice_exists:
        institution_text = "The Institution Notices are for use by collecting institutions, data repositories and organizations who engage in collaborative curation with Indigenous and other marginalized communities who have been traditionally excluded from processes of documentation and record keeping.\nThe Institution Notices are intended to be displayed prominently on public-facing institutional websites, on digital collections pages and or in finding aids."
        notice_text = "The BC, TK and Attribution Incomplete Notices are specific tools for institutions and researchers which support the recognition of Indigenous interests in collections and data. The Notices are a mechanism for researchers and institutional staff to identify Indigenous collections and Indigenous interests in data.\n\nThe Notices can function as place-holders on collections, data, or in a sample field until a TK or a BC Label is added by a community."
        readme_text = notice_text + '\n\n' + institution_text + '\n\nThis folder contains the following files:\n'

    # Create PDF from project context, append to files list
    pdf = render_to_pdf(template_path, context)
    files.append(('Project_Overview.pdf', pdf))

    # Label / Notice Files
    if notice_exists:
        notices = Notice.objects.filter(project=project)
        for notice in notices:
            if not notice.archived:
                # Create PNG and TXT files based on which Notices are attached to the Project
                if notice.notice_type == 'biocultural':
                    get_img = requests.get(notice.img_url)
                    get_svg = requests.get(baseURL + 'labels/notices/bc-notice.svg')
                    files.append(('Biocultural_Notice' + '.png', get_img.content))
                    files.append(('Biocultural_Notice' + '.svg', get_svg.content))
                    files.append(('Biocultural_Notice' + '.txt', notice.default_text))

                if notice.notice_type == 'traditional_knowledge':
                    get_img = requests.get(notice.img_url)
                    get_svg = requests.get(baseURL + 'labels/notices/tk-notice.svg')
                    files.append(('Traditional_Knowledge_Notice' + '.png', get_img.content))
                    files.append(('Traditional_Knowledge_Notice' + '.svg', get_svg.content))
                    files.append(('Traditional_Knowledge_Notice' + '.txt', notice.default_text))
                
                if notice.notice_type == 'attribution_incomplete':
                    get_img = requests.get(notice.img_url)
                    get_svg = requests.get(baseURL + 'labels/notices/ci-attribution-incomplete.svg')
                    files.append(('Attribution_Incomplete' + '.png', get_img.content))
                    files.append(('Attribution_Incomplete' + '.svg', get_svg.content))
                    files.append(('Attribution_Incomplete' + '.txt', notice.default_text))

    if project_bclabels or project_tklabels:
        # Set readme text
        readme_text = "The Traditional Knowledge (TK) and Biocultural (BC) Labels reinforce the cultural authority and rights of Indigenous communities. \nThe TK and BC Labels are intended to be displayed prominently on public-facing Indigenous community, researcher and institutional websites, metadata and digital collection's pages.\n\nThis folder contains the following files:\n"

    # Add Label images, text and translations
    for bclabel in project_bclabels:
        get_image = requests.get(bclabel.img_url)
        get_svg = requests.get(bclabel.svg_url)
        files.append((bclabel.name + '.png', get_image.content))
        files.append((bclabel.name + '.svg', get_svg.content))

        # Default Label text
        text_content = bclabel.name + '\n' + bclabel.label_text
        text_addon = []

        if bclabel.bclabel_translation.all():
            for translation in bclabel.bclabel_translation.all():
                text_addon.append('\n\n' + translation.translated_name + ' (' + translation.language + ') ' + '\n' + translation.translated_text)
            files.append((bclabel.name + '.txt', text_content + '\n'.join(text_addon)))
        else:
            files.append((bclabel.name + '.txt', text_content))

    # Add Label images, text and translations
    for tklabel in project_tklabels:
        get_image = requests.get(tklabel.img_url)
        get_svg = requests.get(tklabel.svg_url)
        files.append((tklabel.name + '.png', get_image.content))
        files.append((tklabel.name + '.svg', get_svg.content))
        
        # Default Label text
        text_content = tklabel.name + '\n' + tklabel.label_text
        text_addon = []

        if tklabel.tklabel_translation.all():
            for translation in tklabel.tklabel_translation.all():
                text_addon.append('\n\n' + translation.translated_name + ' (' + translation.language + ') ' + '\n' + translation.translated_text)
            files.append((tklabel.name + '.txt', text_content + '\n'.join(text_addon)))
        else:
            files.append((tklabel.name + '.txt', text_content))
    
    # Create Readme
    file_names = []
    for f in files:
        file_names.append(f[0])
    readme_content = readme_text + '\n'.join(file_names) + '\n\nRefer to the Usage Guides (https://localcontexts.org/support/downloadable-resources/) for details on how to adapt and display the Notices or Labels for your Project.\n\nFor more information, contact Local Contexts at localcontexts.org or support@localcontexts.org'
    files.append(('README.txt', readme_content))

    # Generate zip file 
    full_zip_in_memory = generate_zip(files)

    zipfile_name = f"LC-Project-{project.title}.zip"

    response = HttpResponse(full_zip_in_memory, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(zipfile_name)

    return response
