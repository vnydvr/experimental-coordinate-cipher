# experimental-coordinate-cipher
Experimental stateful position-based message encoding scheme
# Experimental Coordinate-Based Cipher

This repository contains an **experimental message encoding scheme**
based on transmitting **positions (coordinates)** within a shared
deterministic sequence instead of transmitting ciphertext directly.

⚠️ **This is NOT production cryptography.**  
The project is intended for research, learning, and architectural exploration.

---

## Core Idea

Instead of encrypting symbols into other symbols, this scheme:

- Generates a shared deterministic sequence from a secret key
- Encodes messages as **positions of matching blocks** inside that sequence
- Evolves internal state after each message (stateful / lockstep protocol)
- Never reuses the same state twice
- Transmits only numeric coordinates

As a result:
- There is no fixed symbol-to-cipher mapping
- Identical messages never look the same
- Classical frequency analysis does not directly apply

---

## High-Level Properties

- **Stateful communication** (both sides stay in sync)
- **Evolving shared state** after every message
- **Position-based encoding**, not value-based encryption
- **Explicit resynchronization mechanism** (`reset`)
- Deterministic behavior given the same key and state

---

## What This Project Is

✔ An experimental cipher design  
✔ A protocol design exercise  
✔ A learning project in cryptographic thinking  
✔ A demonstration of stateful encoding ideas  
✔ A portfolio / research project  

---

## What This Project Is NOT

❌ Not certified cryptography  
❌ Not audited  
❌ Not formally proven secure  
❌ Not suitable for real-world secure communications  
❌ Not a replacement for AES, ChaCha20, Signal, etc.

---

## Security Notes (Important)

- The randomness source used in this implementation is **not cryptographically proven**
- No formal security reduction is provided
- The scheme has not been reviewed by cryptographers
- Do **not** use this software to protect sensitive or safety-critical data

This project intentionally prioritizes **architectural exploration**
over formal cryptographic guarantees.

---

## Supported Features

- Text-based CLI interface
- Strict lockstep protocol (send ↔ receive)
- Automatic filtering of unsupported characters
- Padding for odd-length messages
- Emergency resynchronization via `reset`
- Deterministic decoding given correct state

Supported characters:
a-z, 0-9, space, . , ? ! : - " '

---

## Motivation

The project explores the question:

> *What happens if messages are transmitted as coordinates inside a
shared evolving space rather than as encrypted symbols?*

This idea draws inspiration from historical stateful cipher machines
and modern stream-based cryptographic thinking, while remaining
explicitly experimental.

---

## Implementation Notes

- Written in Python
- Uses high-precision arithmetic for deterministic sequence generation
- Focuses on correctness and clarity rather than performance
- Designed to be readable and modifiable

---

## Authorship

Architecture and protocol design by the author.  
Implementation developed with **AI-assisted coding**.

---

## License

MIT License
