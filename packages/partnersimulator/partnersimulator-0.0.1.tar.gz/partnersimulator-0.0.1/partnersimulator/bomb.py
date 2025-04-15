import os

import polars as pl
import json
json_path = 'samantha20.json'

adding_df = pl.DataFrame(
    data={'name':['donut'],
          'height':[13.4]}
)
print(adding_df)

if os.path.exists(json_path):
    df = pl.read_json(json_path)
else:
    raise RuntimeError('sorry, the specified path does not exist')
print(df)

concated_df = pl.concat([df, adding_df], how='vertical_relaxed')
print(concated_df)

concated_df.write_json('bingo.json')
