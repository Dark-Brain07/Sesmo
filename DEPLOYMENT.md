# Deployment and live evidence

## Canonical network

- GenLayer Studionet, chain ID **61999**
- RPC: <https://studio.genlayer.com/api>
- Explorer: <https://explorer-studio.genlayer.com>
- Stable GenLayer CLI 0.39.1; GenVM lint v0.2.16 / genvm-linter 0.11.0.

`python scripts/check_network.py` independently returned `chain id: 61999` before live transactions. It refuses deployment/testing if the RPC cannot prove this exact chain.

## Final deployments

| Contract | Address | Deployment transaction | Finality | Repository source SHA-256 |
|---|---|---|---|---|
| SESMO | `0xE11a1E08232d940b141CeC240a77AC6f6F73Da44` | `0x6d3790d10d6646dbd1e74511e30e7652e81eecee8f0405f7723d7b3410a9e8d2` | FINALIZED, MAJORITY_AGREE (5/5) | `fd38e67b638ee8d16130178efef920a91ed8ae79a359608afc7e56fcc8ad1b81` |
| ExampleSesmoedGrant | `0x996a8D081EF5842335915CF0b63Ea24Ab968d375` | `0x3588f6e2bee52e003f1c8c377503dc19af45e2bc0cb50c10f27863a9e4ba1b52` | FINALIZED, MAJORITY_AGREE (5/5) | `299e44ec32d6bbb154d45c516f612073aee4548e2fe0f221e57e870b270c17c0` |

The consumer constructor points to the finalized SESMO above. `genlayer code` fetched each deployed contract. Both fetched responses contain the complete corresponding repository source byte-for-byte (the CLI adds a `Result:` wrapper and leading newline). Repository source lengths are 44,844 bytes and 13,552 bytes respectively. The exact Git commit for these sources is the commit that records this evidence; source hashes are listed above.

## Live COMMIT lifecycle (final deployment, sesmo 2 / grant 1)

- Create sesmo: `0x8ede32a14974b0dcb0bd355984f6ce75ba639b11789a859e5b69f762bed408a8`
- Stage provisional grant: `0x0978622c48562c79e6d8320b6ffffe6880b4947f4e5a5d925bd1d364ecc856a2`
- Finalized consumer arm child: `0x9785656a6b6ec42b8be93ed00b9928e5ccb102d0f1c1ad9165bff71bbda91edb`
- Resolve SATISFIED: `0xf694a01d9b011522627bbaa29078c651b2fa6f2084a12eb346dcf7711c48f16e`
- Finalized `sesmo_commit` child: `0x5d2668de4747daab02c6d242b9165c26a0b0bacb4263f48253cb5cbc5d8ef400`
- Finalized consumer acknowledgement: `0x180d8776d3774da984a621e14b3e603a059c5589a80ada0f0788a17c230d9f4e`
- Read-back: SESMO `COMMITTED`, attempt `SATISFIED`, grant `COMMITTED`, usable credit 0→5, acknowledgement `COMMITTED`. All parent and child transactions finalized with MAJORITY_AGREE.

## Live FAILED lifecycle (final deployment, sesmo 3 / grant 2)

- Create sesmo: `0x273ad7b5c454cc5a3659cbf2014329e4b0fab30ba1025191abd8579e440959be`
- Stage provisional grant: `0x6a8f9e0fe894aa303077aff521d8f4d9770fec29ba281232bbd7137c7abc68db`
- Finalized consumer arm child: `0x6275638a48d436b30ea73dd3cb7457a6139e7b09635e0d86ee46b9680d136876`
- Resolve FAILED: `0xa434c8c91799a49e320d88d2dc39a2a660fb0961dff81555067d9c738b87999c`
- Finalized `sesmo_revert` child: `0x18b260b822ae54b84e1ddba4512799f19a940a203ae3e82179992b53bc340e82`
- Finalized consumer acknowledgement: `0xc3ec14edebb3738e3dfe0f464fea5b2cd76d180b896159d95fa70e74b2ef2eff`
- Read-back: SESMO `REVERT_REQUIRED`, outcome `FAILED`, grant `REVERTED`, acknowledgement `REVERTED`. The grant's provisional amount never became usable; usable credit remained 5 from the earlier committed grant. All parent and child transactions finalized with MAJORITY_AGREE.

The public fixtures are synthetic protocol test data, not claims about a real service or customer. Source quotes and the frozen conditions are recorded on chain.

## Source review and local validation

- Source identity: SESMO SHA-256 `fd38e67b638ee8d16130178efef920a91ed8ae79a359608afc7e56fcc8ad1b81`; consumer SHA-256 `299e44ec32d6bbb154d45c516f612073aee4548e2fe0f221e57e870b270c17c0`.
- `python scripts/preflight.py`: PASS.
- `python scripts/source_manifest.py`: PASS.
- `python -m pytest tests/direct -v`: 38 passed.
- GenVM lint and semantic validation: SESMO 15 methods (8 views, 7 writes) PASS; consumer 7 methods (3 views, 4 writes) PASS.
- Both contract source files remain bounded (44,844 and 13,552 bytes).

## Value and fees

Transactions sent zero GEN application value. The stable RPC returned `eth_gasPrice=0x0` and generic `eth_estimateGas=0x7a120`; neither is a reliable settled fee quote. Receipts expose gas limits and leader VM gas usage, not settled fee/refund. No transaction fee is invented or inferred from those fields.

## GitHub

Final repository target: `https://github.com/Dark-Brain07/Sesmo.git`, branch `main`. No other remote is authorized or configured.
