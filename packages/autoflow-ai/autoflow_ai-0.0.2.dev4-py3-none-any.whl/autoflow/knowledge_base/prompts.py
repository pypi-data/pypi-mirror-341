from llama_index.core.prompts.rich import RichPromptTemplate

QA_WITH_KNOWLEDGE_PROMPT_TEMPLATE = RichPromptTemplate(
    template_str="""
    {% chat role="system" %}
    We have provided context information below.
    ---------------------
    {% if knowledge_graph %}
    <knowledge_graph>
        <entities>
            {% for entity in knowledge_graph %}
            <entity id="{{ entity.id }}">
            {{ entity.name }}: {{ entity.description }}
            </entity>
            {% endfor %}
        </entities>
        <relationships>
            {% for relationship in knowledge_graph %}
            <relationship id="{{ relationship.id }}">
            {{relationship.source_entity.name}} -> {{ relationship.description }} -> {{relationship.target_entity.name}}
            </relationship>
            {% endfor %}
        </relationships>
    </knowledge_graph>
    {% endif %}

    {% for chunk in chunks %}
    <chunk id="{{ chunk.id }}">
    {{ chunk.text }}
    </chunk>
    {% endfor %}
    ---------------------
    Given this information, please answer the question: 
    {% endchat %}

    {% chat role="user" %}
    {{ query_str }}
    {% endchat %}
    """
)