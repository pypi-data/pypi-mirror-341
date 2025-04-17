from sier2 import Info

def blocks() -> list[Info]:
    return [
        Info('sier2_blocks_datamap.blocks:RunUMAP', 'Run data through UMAP to reduce dimensionality.'),
        Info('sier2_blocks_datamap.blocks:ThisNotThat', 'Show a ThisNotThat interactive plot.'),
    ]

def dags() -> list[Info]:
    return [ 
        Info('sier2_blocks_datamap.dags:datamap', 'Load a dataframe and make a datamap'),
    ]
