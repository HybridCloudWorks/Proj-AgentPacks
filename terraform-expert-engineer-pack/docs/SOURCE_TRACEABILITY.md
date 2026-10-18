# Source Traceability

All supplied documents were read as reference material. Exact duplicates are retained in this ledger and consolidated in the canonical source; no source was silently discarded.

## Terraform engineer source set

| Source | SHA-256 | Disposition |
|---|---|---|
| terraform-engineer.agent.md | 3EB7E2B888AA708D19E7BE42BC366E5920B7AC32F3CF27C51E916C6DD0460F6B | Canonical source for broad Terraform mission, state, backend, provider-agnostic design, safety, and operating rules. |
| terraform-engineer.md | D3707ACCB1FF958F7DAF0D1CB52A72659A9BBFBCBEE89093B7F971B7155BA1BB | Source for Terraform craft, module quality, tests, policy, Stacks, registry, import, trade-offs, and maturity. |
| terraform-engineer (2).md | A1C76041C9F40F6F4C569AAA725AD0055407C95854681571E549D9B96426B0FB | Byte-distinct duplicate export of terraform-engineer.md; content consolidated with that source. |
| terraform-module-engineer.md | E949B7DCE4231D61B9A629AE15E44D368C52D11C97D2DDB4C9A13E9784938D2A | Source for module boundaries, generator context, AVM use, pinned registry sources, state, OIDC, and refactoring workflow. |
| SKILL.md | 7484A3B1139F99E37D0F082C9B9F636DFD6FC04CE7342197B2AFC81AE2C0F8A1 | Azure AVM requirements source; consolidated with three exact duplicates. |
| SKILL (2).md | 417FB3A37099A54562253EDD6046EBB4A73066551D3D0E5C7DA7F4E8CD402EE0 | Byte-identical AVM duplicate. |
| SKILL (3).md | 417FB3A37099A54562253EDD6046EBB4A73066551D3D0E5C7DA7F4E8CD402EE0 | Byte-identical AVM duplicate. |
| SKILL (4).md | 417FB3A37099A54562253EDD6046EBB4A73066551D3D0E5C7DA7F4E8CD402EE0 | Byte-identical AVM duplicate. |
| SKILL (5).md | 04526DDC20A2252A82DD3C6FF17C55C724BEB31D54A6238CC4A3DC5832F16488 | Cloud-specific Terraform examples; high-level resource and secret patterns retained as context, not as a mandatory provider scope. |
| SKILL (6).md | C5E042F70FB7BEA59F1F7DB1A36814B1FB42B800557C508675406322D9011845 | Provider scaffolding and Go development source; consolidated into terraform-provider-development. |
| SKILL (7).md | 931968B0BD5703A2FA6E56F7D638AA50079F5BCB40CB276A043D26BE77610CA6 | Terraform policy router; consolidated with tfpolicy author/test material. |
| SKILL (8).md | 89B59E1B08640372F9E3E5DEA689234DA93863FCC5AE5ABC4D736CDA8CDAE873 | Terraform test framework source; consolidated with mock and CI references. |
| SKILL (9).md | FDB7A6BB4E1E234D20EBC6BE582078E68114B962A953DBAAF1CD8ECF8A4B6279 | Terraform style source; consolidated into terraform-core-and-style. |
| SKILL (10).md | E22F6E7920A9558D96D90AAD2AE735F14BABB87E98D151F03843BE65F9C8B2E1 | Terraform Stacks source; consolidated into terraform-cloud-and-stacks. |
| SKILL (11).md | 62A90B9582B5BAE3579FAECE7B25A912A01B71D8E78677C8DC4A3C2F24145289 | Terraform Search and bulk import source; consolidated into terraform-state-backends-and-imports. |
| tfpolicy-author.md | FCCA082AB98B4536CD9A2D29291A8B686A46F9FDA445DFFE9FC2FCC89AE19634 | Policy authoring and Sentinel conversion source. |
| tfpolicy-test.md | 9B12FB3D40BE07F091E1F8FC7F084A970A3076A15C8353F8B9F955E67280C1E6 | Policy test and mock behavior source. |
| verified-syntax.md | B2372B23355BCAD08E331AA3CCBACCA4D137F8C034A7615652FA210BED934F85 | Version-sensitive tfpolicy syntax source; retained as a caution to validate the installed product version. |
| troubleshooting.md | 2D6F7AB949033270C1F08281E007D2237D8008F944D7C8AF83CDAE5E958EB701 | Troubleshooting examples; folded into core and lifecycle guidance. |
| CI_CD.md | BF0F9E39DA4AB5112A2C696F5A34BD23B6A38C59124077B0E543D30555356343 | CI ordering and test-stage source. |
| MOCK_PROVIDERS.md | 921E5B7AD34AF748D35470E7F040F28B2C04A7437DC57DBEC5990A16E34721DA | Mock provider examples and limitations. |
| MANUAL-IMPORT.md | 7AE0EB8176370B337507DA1D5973B15557D2D420693CABA12AFEB0BA3673029D | Manual and declarative import source. |
| linked-stacks.md | 3E3E8442F1C770FBE3835A8CDFC87286CF2F7E5B630871125DF5133859BC043B | Linked Stack output/input source. |
| SECURITY.md | 8DDF2CFDBEF349E117E128280620D7A215EA4F46FA421EF866E7699637276ED2 | Terraform security style source. |
| main.go | FE2C1C7B14DAEC92F130AD73F21FC38BBABBFEE59B01011EB91FEFD3C27B174F | Provider server example. |
| main.go.example | FE2C1C7B14DAEC92F130AD73F21FC38BBABBFEE59B01011EB91FEFD3C27B174F | Byte-identical provider server example. |
| list_resources.sh | 8325FBF9E82E8B4AB1D281C02AD7058220A82878278A7F004C92F899167C79EA | Provider discovery helper; represented as workflow guidance, not executed. |
| eval.yaml | 5A1BADF8891BB0FDA2B297A0740A3E059A7D2012AF07ACC1E9F5EAD2DEC6D3B9 | Evaluation metadata; used to inform trigger and coverage testing. |
| positive-trigger-1.yaml | BFE1CEA6EBE1F14B26C6387BB24C7CEE41135DCE482C0CAF332FDB42A7C6254A | Positive trigger example. |
| positive-trigger-2.yaml | 8A51F333D98B7BB49BE9702890DCA1BF9404EA7C7F970BE8258469D84B6E1E3E | Positive trigger example. |
| negative-trigger-1.yaml | 02850879C0299B37D880BF5E8D7EF84A8259C9FA325774A6FAA56590CDB2D7E6 | Negative trigger example. |
| examples (2).md | F11F334E0A87CF459475DDFFB5881424FE7E1AC47A2D1FE99AF148C3BF13A804 | Terraform Stacks examples; consolidated into Stack routing and test cases. |
| EXAMPLES.md | 554C81CF4B0B7560A093E148B2934F8FA976B4B60DCEF6BBA7B88DD67504E97A | Terraform test examples; consolidated into testing guidance. |
| README.md | 3D60529A857E387E0C0983C572FA7C5C005D1DBF6AC76A81EF86DAC97AD83E56 | Policy pack overview and routing. |
| README (2).md | 702F0DC4B5620DCAE346615300706DF7D6A32F83E41E927647BC9B9635D2850C | Sentinel-to-tfpolicy conversion example; consolidated as examples and limitations. |
| README (3).md | 4F28501FEA13D3C29FE056E514CD4C3AF2D92846585B4CBEFFEECD8AF2AAFAFE | Sentinel-to-tfpolicy conversion example; consolidated as examples and limitations. |
| README (4).md | 722884F6087E516BF7D9144442C0F548371C624BDBABDCABEA2556180AAD2E75 | Sentinel-to-tfpolicy conversion example; consolidated as examples and limitations. |
| README (5).md | AEDEC788241960A0EADFC82F19BECF6B369172A88C611CD7065F59B8540C5D4E | Sentinel-to-tfpolicy conversion example; consolidated as examples and limitations. |
| README (6).md | BE94AB604B9F12BE0A20A9C9B275268F1AF197CC44333F4D173FE065B1B73AFF | Sentinel-to-tfpolicy conversion example; consolidated as examples and limitations. |
| README (7).md | B10A89B7D9482EF79DA36DB75AAEAE37D1CF3EE190EAAEB53B4E166A751DA9A9 | Sentinel-to-tfpolicy conversion example; consolidated as examples and limitations. |
| README (8).md | 052C4980A375C64ED40F9A29CB6F4AC7CAE7CAFABB25693E19A9DBD5A0D7A09C | Sentinel-to-tfpolicy conversion example; consolidated as examples and limitations. |
| README (9).md | 3C4A430DB816F3F9B91E33220825F1AABF2801C5C9EAD8B5013B9B1A7C4 | Sentinel-to-tfpolicy conversion example; consolidated as examples and limitations. |
| README (10).md | 31AEAFAABE7610664451E23EC66E395428E1D87BE4EC8DD21D3F962C016CD961 | Sentinel-to-tfpolicy conversion example; consolidated as examples and limitations. |
| README (11).md | CAE7DE5D00FC13874A7E1CF0EB847B7DBE08167A54C8137D973E05D06DB4C0AA | Sentinel-to-tfpolicy conversion example; consolidated as examples and limitations. |
| README (12).md | 614C227D649B8CAA9E7A1B1DCFF711A688552C7F1BAF21B02E4D43DF9BABA9F7 | Conversion example index and quality labels. |

## Additional supplied sources

| Source | SHA-256 | Disposition |
|---|---|---|
| Azure ALZ Architect/azure-verified-modules/SKILL.md | 7484A3B1139F99E37D0F082C9B9F636DFD6FC04CE7342197B2AFC81AE2C0F8A1 | Same AVM source as the Terraform folder; consolidated once. |
| Azure ALZ Architect/azure-verified-modules/SKILL (2).md | 417FB3A37099A54562253EDD6046EBB4A73066551D3D0E5C7DA7F4E8CD402EE0 | Byte-identical AVM duplicate. |
| Azure ALZ Architect/azure-verified-modules/SKILL (3).md | 417FB3A37099A54562253EDD6046EBB4A73066551D3D0E5C7DA7F4E8CD402EE0 | Byte-identical AVM duplicate. |
| Azure ALZ Architect/azure-verified-modules/SKILL (4).md | 417FB3A37099A54562253EDD6046EBB4A73066551D3D0E5C7DA7F4E8CD402EE0 | Byte-identical AVM duplicate. |
| Cloud Standardization Architect/iac-repo-standardizer.md | 3425A4CADCAF3D57E7A6D06065617B31E71E59599DEA8AE91C035BDB348D95E2 | Repository standardization source; used for repository-neutral structure, not copied as Terraform policy. |
