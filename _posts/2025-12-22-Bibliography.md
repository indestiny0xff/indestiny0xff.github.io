![](https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExbXpwbDU3Zndtc2JvbWhvZ3ZodW15eTV5aGp3Y3hyNnY1OWJwYnptMiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/1Ma50Mm61JVXksISXw/200.webp) 

I will pinpoint in this section all the documentations that have been used to write my technical writeup, it's only to keep track of all the things in case i forget, and it can also be helpful later on for crossing references between them.

---

## Sources
- Checkpoint
- Silentpush
- Hasherezade
- Smukx aka Whitecat18


--- 

## Topics Ideas :  
-  Tracking infrastructure : [BPH](https://info.silentpush.com/hubfs/SP-WP-bulletproof-hosting.pdf?utm_campaign=31865988-asset-bph-whitepaper-q4fy25&utm_source=website&utm_medium=post)
  - [ ] Retrieve DROP from shse, monitor any change in DNS record 
  - [ ] Match Discovered ASNs with hurricane electric database to see if they any peering partner ?
  - [ ] Look for indicator for BPH : Crescendo (Whois DNS ASN Organisations records, patterns in domains/ structure of the hosted pages (find a common skeleton ?), pattern on contents (what can be useful and what is impratical for our use cases)
  - [ ] Test for various kinds of tools (also creating somes) (for the tests: take a random bph range of ip)

-  Detection / threat hunting : Oneshot honeypotlab
  - [ ] Write a oneshot script for the deployement of the lab (Ansible, bash ? ...)
  - [ ] Incorporate at least 3 types of motors : Suricata, yara, sigma
  - [ ] Find the best cost effective infra

-  Reverse engineering and Malware Analysis : [Rust for maldev](https://github.com/indestiny0xff/Rust-for-Malware-Development/tree/main) , [Hasherezade  repo](https://github.com/hasherezade)
  - [ ] Writeup about Struppigel courses ? MAOS books?
  - [ ] Create a repo with several languages : Language_name - malware types - malware variant - malware techniques.
  - [ ] Developping tools to automate manuals tasks (Go/Rust/Python)
