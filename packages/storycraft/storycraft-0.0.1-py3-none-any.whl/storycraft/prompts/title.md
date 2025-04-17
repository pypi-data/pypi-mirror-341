Generate a new title for the novel.

{% if title is defined and title %}
The current title is: {{ title }}.

If you think the current title matches the outline, output it, otherwise output a better title.
{% endif %}

Just output the title, nothing more, no quotes arund the title.