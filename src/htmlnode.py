class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Child classes are expected to implement this")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return ' ' + " ".join([f'{key}="{self.props[key]}"' for key in self.props])
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"