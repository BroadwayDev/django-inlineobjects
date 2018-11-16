from django.template import TemplateSyntaxError
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.utils.encoding import smart_text
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


def inlines(value, return_list=False):
    try:
        print("7")
        from bs4 import BeautifulSoup
    except ImportError:
        print("8")
        pass

    content = BeautifulSoup(value, 'html')

    # Return a list of inline objects found in the value.
    if return_list:
        print("9")
        inline_list = []
        for inline in content.findAll('inline'):
            rendered_inline = render_inline(inline)
            inline_list.append(rendered_inline['context'])
        print("10")
        print(inline_list)
        return inline_list

    # Replace inline markup in the value with rendered inline templates.
    else:
        print("11")
        for inline in content.findAll('inline'):
            rendered_inline = render_inline(inline)
            if rendered_inline:
                inline_template = render_to_string(rendered_inline['template'],
                                                   rendered_inline['context'])
            else:
                inline_template = ''
            value = value.replace(str(inline), inline_template)
        print("12")
        print(mark_safe(str(value)))
        return mark_safe(str(value))


def render_inline(inline):
    print("In render_inline")
    """
    Replace inline markup with template markup that matches the
    appropriate app and model.
    """

    # Look for inline type, 'app.model'
    try:
        print("1")
        app_label, model_name = inline['type'].split('.')
    except:
        if settings.DEBUG:
            raise TemplateSyntaxError("Couldn't find the attribute 'type' in "
                                       "the <inline> tag.")
        else:
            return ''

    # Look for content type
    try:
        print("2")
        content_type = ContentType.objects.get(app_label=app_label,
                                               model=model_name)
        model = content_type.model_class()
    except ContentType.DoesNotExist:
        if settings.DEBUG:
            raise TemplateSyntaxError("Inline ContentType not found.")
        else:
            return ''

    # Create the context with all the attributes in the inline markup.
    print("3")
    context = dict((attr[0], attr[1]) for attr in inline.attrs)
    print(context)

    # If multiple IDs were specified, build a list of all requested objects
    # and add them to the context.
    try:
        try:
            print("4")
            id_list = [int(i) for i in inline['ids'].split(',')]
            obj_list = model.objects.in_bulk(id_list)
            obj_list = list(obj_list[int(i)] for i in id_list)
            context['object_list'] = obj_list
            print(context)
        except ValueError:
            if settings.DEBUG:
                raise ValueError("The <inline> ids attribute is missing or "
                                 "invalid.")
            else:
                return ''

    # If only one ID was specified, retrieve the requested object and add it
    # to the context.
    except KeyError:
        try:
            print("5")
            obj = model.objects.get(pk=inline['id'])
            context['object'] = obj
            context['settings'] = settings
            print(context)
        except model.DoesNotExist:
            if settings.DEBUG:
                raise model.DoesNotExist("%s with pk of '%s' does not exist"
                                         % (model_name, inline['id']))
            else:
                return ''
        except:
            if settings.DEBUG:
                raise TemplateSyntaxError("The <inline> id attribute is "
                                          "missing or invalid.")
            else:
                return ''

    # Set the name of the template that should be used to render the inline.
    print("6")
    template = ["inlines/%s_%s.html" % (app_label, model_name),
                "inlines/default.html"]

    # Return the template name and the context.
    return {'template': template, 'context': context}
