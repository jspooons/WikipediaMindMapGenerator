# WikipediaTopicMindMapGenerator

Creates a mind map for any wikipedia page
- webscrapes wikipedia pages and creates a hierarchical dictionary
- the dictionary is then pre-processed
- each section is trained on an individual Latent Dirichlet Allocation model
- the topics from each LDA model are then saved for each section
- graphvis is used to generate the mindmap

In some cases, some wikipedia pages will fail to generate mind maps if some sections are too small, in thise case:
- in `build_ngrams()`, adjust:
  - min_count, threshold
- or/and in the `generate_lda_parameters()`, adjust:
  - no_below, no_above
