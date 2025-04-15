from rachord import Chord


def test_smoke(tmpdir):
    adjacency_matrix = [
        [0, 1, 1, 1, 4],
        [1, 0, 1, 7, 2],
        [1, 1, 0, 5, 10],
        [1, 7, 5, 0, 2],
        [4, 2, 10, 2, 0],
    ]
    labels = ["Laplus", "Lui", "Koyori", "Chloe", "Iroha"]

    fig = Chord(adjacency_matrix, labels)
    fig.save_svg(tmpdir / "chord.svg")
