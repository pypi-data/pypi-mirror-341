Write the content of the section {{ index + 1 }} of the novel.
Just write the content, no title, no other text. At least {{ chapter_size }} words.

{% if prompt is defined and prompt %}
User's additional instructions:

{{ prompt }}
{% endif %}

Chapter Title: {{ title }}

Chapter Outline:

{{ outline }}
