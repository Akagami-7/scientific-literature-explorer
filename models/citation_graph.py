import networkx as nx
import matplotlib.pyplot as plt


class CitationGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def clear(self):
        """Reset the graph."""
        self.graph.clear()

    def build_star_graph(self, main_paper_title, citations):
        """
        Creates a star graph:
        Main Paper -> Cited Papers
        """
        self.clear()

        # Add main node
        self.graph.add_node(
            main_paper_title,
            color="red",
            size=2500
        )

        # Add citation nodes
        for idx, cit in enumerate(citations, start=1):
            label = f"Ref [{idx}] {cit}"
            self.graph.add_node(
                label,
                color="skyblue",
                size=1200
            )
            self.graph.add_edge(main_paper_title, label)

        return self.graph

    def add_citation(self, citing_paper, cited_paper):
        """
        Add a single citation edge:
        citing_paper -> cited_paper
        """
        self.graph.add_edge(citing_paper, cited_paper)

    def compute_basic_stats(self):
        """
        Returns basic graph statistics.
        """
        return {
            "num_nodes": self.graph.number_of_nodes(),
            "num_edges": self.graph.number_of_edges(),
            "density": nx.density(self.graph),
        }

    def get_matplotlib_figure(self):
        """
        Returns a matplotlib figure (for Streamlit rendering).
        """
        if self.graph.number_of_nodes() == 0:
            return None

        fig, ax = plt.subplots(figsize=(9, 7))
        pos = nx.spring_layout(self.graph, seed=42)

        # Extract node attributes safely
        colors = [
            self.graph.nodes[n].get("color", "skyblue")
            for n in self.graph.nodes
        ]

        sizes = [
            self.graph.nodes[n].get("size", 1000)
            for n in self.graph.nodes
        ]

        nx.draw(
            self.graph,
            pos,
            ax=ax,
            with_labels=True,
            node_color=colors,
            node_size=sizes,
            font_size=9,
            arrows=True
        )

        ax.set_title("Citation Network")
        return fig
