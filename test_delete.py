class Graph:
    def __init__(self, key, display_name, header, description, type):
        self.key = key
        self.display_name = display_name
        self.header = header
        self.description = description
        self.type = type

class Section:
    def __init__(self, key, display_name, header, description):
        self.key = key
        self.display_name = display_name
        self.header = header
        self.description = description
        self.graphs = []

    def add_graph(self, graph):
        self.graphs.append(graph)

class Category:
    def __init__(self, key, display_name, header, description):
        self.key = key
        self.display_name = display_name
        self.header = header
        self.description = description
        self.sections = []

    def add_section(self, section):
        self.sections.append(section)

class DataStructure:
    def __init__(self):
        self.categories = []

    def add_category(self, category):
        self.categories.append(category)

# Example usage
data_structure = DataStructure()

category1 = Category("cat1", "Category 1", "Header 1", "Description 1")
section1 = Section("sec1", "Section 1", "Section Header 1", "Section Description 1")
graph1 = Graph("graph1", "Graph 1", "Graph Header 1", "Graph Description 1", print())
section1.add_graph(graph1)
category1.add_section(section1)

category2 = Category("cat2", "Category 2", "Header 2", "Description 2")
section2 = Section("sec2", "Section 2", "Section Header 2", "Section Description 2")
graph2 = Graph("graph2", "Graph 2", "Graph Header 2", "Graph Description 2")
section2.add_graph(graph2)
category2.add_section(section2)

data_structure.add_category(category1)
data_structure.add_category(category2)

# Iterating through categories, sections, and graphs
for category in data_structure.categories:
    print("Category:", category.display_name)
    for section in category.sections:
        print("  Section:", section.display_name)
        for graph in section.graphs:
            print("    Graph:", graph.display_name)
            var = "type"
            output = getattr(graph, var)
            print()

print("hiiii")
