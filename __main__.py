from subject import Subject
from SpaceLeaper.graph_initialization import create_synergy_graph


def main() -> None:
    graph = create_synergy_graph()
    graph.print_subjects()


if __name__ == "__main__":
    main()
