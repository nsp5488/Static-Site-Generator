from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            print(self)
            raise ValueError("Invalid leaf node! Leaf Nodes must have a value")
        if self.tag is None:
            return self.value

        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"
