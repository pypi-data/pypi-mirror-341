## v3.9.0 (2025-04-16)

### ✨ Features

- **io.dataloader:** implement loader-based parallel keyword arguments ([ea8cfc6](https://github.com/kmnhan/erlabpy/commit/ea8cfc6d150a942d9c9b6bc5beaea8019e2ec335))

  Allows plugins to pass different keyword arguments to `joblib.Parallel` by setting the `parallel_kwargs` class attribute.

- **ktool:** set default angle offsets to coordinate values ([a8115d0](https://github.com/kmnhan/erlabpy/commit/a8115d05122b08311ec60fe1dbb64f835f22e4a9))

- **ktool:** show current configuration in KspaceTool GUI ([907aeb9](https://github.com/kmnhan/erlabpy/commit/907aeb995a4c8a4445209b20c77f7bf06dd7701b))

- **analysis.image:** add function to remove energy-independent 'stripe' artifacts (#122) ([028239e](https://github.com/kmnhan/erlabpy/commit/028239ee4ef41a33ba57a494eee60b519b8c0aee))

### 🐞 Bug Fixes

- **io.dataloader:** enhance value formatting for native datetime coordinates in summary ([f79bce5](https://github.com/kmnhan/erlabpy/commit/f79bce5de9eb1a923655e846385fbdbc84dfa9e9))

- **io.plugins.erpes:** fix summary generation ([598fb2d](https://github.com/kmnhan/erlabpy/commit/598fb2d68a612b373493f7ce12ba9f1d69bde0ec))

- **utils.formatting:** improve value formatting for various types and enhance datetime handling ([7e34614](https://github.com/kmnhan/erlabpy/commit/7e3461472d713eec53ef1012998c3ea1b053030d))

- **ktool:** properly set initial bounds and resolution ([5abf988](https://github.com/kmnhan/erlabpy/commit/5abf9880e165b12bf70de2d15fbdb94129c2b2f2))

- **ktool:** expand offset spin box range from ±180 to ±360 degrees ([6895214](https://github.com/kmnhan/erlabpy/commit/68952147b39d37b0f8d7a9915aa4b6dfb4cf2df7))

- **qsel:** preserve non-averaged coord in multidimensional associated coordinates (#127) ([44ceb7e](https://github.com/kmnhan/erlabpy/commit/44ceb7e328036a7b55e58d6a591c0d927fde5545))

  Fixes an issue where averaging over a dimension with `DataArray.qsel()` or `DataArray.qsel.average()` with multidimensional associated coordinates would average the coordinates over all dimensions instead of averaging over just the specified dimension.

- **utils.formatting:** properly format numpy datetime64 objects ([1c74983](https://github.com/kmnhan/erlabpy/commit/1c7498342aa17e59b1a7d0f128cecd7b4e056bb9))

### ⚡️ Performance

- **io.plugins.erpes:** default to threading ([ebfc527](https://github.com/kmnhan/erlabpy/commit/ebfc527f50b7583b3f3f5139746e074c385477ac))

- **io.plugins.da30:** use `libarchive-c` library if it is installed when loading DA30 zip files ([6b9369f](https://github.com/kmnhan/erlabpy/commit/6b9369fc363ed0c0ba8f99c876251a26b7fe27d6))

### ♻️ Code Refactor

- **kspace:** do not write offset attributes unless explicitly specified ([613820f](https://github.com/kmnhan/erlabpy/commit/613820f80fb667332512d75d3a35e5ca4c999778))

- **io.plugins.erpes:** promote waveplate angle attributes to coordinates ([6920528](https://github.com/kmnhan/erlabpy/commit/6920528ec464873cef1cc8509a0159846cc5601b))

[main 12cc68b] bump: version 3.8.4 → 3.9.0
 3 files changed, 13 insertions(+), 3 deletions(-)

