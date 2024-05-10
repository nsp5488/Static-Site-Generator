from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid ParentNode. tag is required")
        if self.children is None:
            raise ValueError("Invalid ParentNode. children are required")
        
        output = f"<{self.tag}{super().props_to_html()}>"
        for child in self.children:
            output += child.to_html()

        return output + f"</{self.tag}>"
