from django import template

register = template.Library()


@register.filter
def only_active_comments(comments):
    return comments.filter(status =True)



@register.filter
def only_active_comments_count(comments):
    return comments.filter(status=True).count()
