# Worked example: intermittent 522 errors

Request: "Since 09:00 UTC some users get error 522 on `app.example.com`." The user supplied three Ray IDs and put the zone in scope.

1. Frame. Symptom: intermittent 522 on one proxied hostname since 09:00 UTC; other hostnames on the same origin are fine.
2. Changes. The zone's audit log shows no Cloudflare change; the user's change log shows a firewall update on the origin network at 08:55 UTC.
3. Locate the layer. 522 is a Cloudflare error meaning the TCP connection to the origin timed out (confirmed in current troubleshooting documentation). The Ray ID suffixes show two data centers affected and one unaffected.
4. Test. `curl -sI https://app.example.com` through Cloudflare reproduces the 522 roughly one time in three. A direct origin test with `curl --resolve` from an allowed network succeeds every time. The origin's firewall configuration, supplied by the user, allows only part of Cloudflare's published IP ranges: the update replaced the list with an outdated copy.
5. Cause confirmed: connections from Cloudflare addresses missing from the allowlist are dropped, which matches the data centers affected.
6. Fix (outside Cloudflare, owned by the network team): restore the full current list of Cloudflare IP ranges, or switch the origin to Cloudflare Tunnel so no inbound allowlist is needed. Verification: repeat the probe from the affected data centers until 50 consecutive requests succeed.
7. Observability gap: no alert on origin connection errors. Recommendation: a notification on elevated 52x rates for the zone (a Level 2 change).

Report: ANALYSIS_ONLY with evidence labeled by time and environment. After the network team's fix, the agent repeats the probe and reports the result.
