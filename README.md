<h3 align="center">🛠️ swift‑route</h3>

<div align="center">
  <a href="https://github.com/your-org/swift-route"><img src="https://img.shields.io/github/stars/your-org/swift-route?style=flat-square" alt="Stars"/></a>
  <a href="https://github.com/your-org/swift-route/blob/main/LICENSE"><img src="https://img.shields.io/github/license/your-org/swift-route?style=flat-square" alt="License"/></a>
  <a href="https://swift.org"><img src="https://img.shields.io/badge/language-Swift-orange?style=flat-square" alt="Language"/></a>
  <a href="https://github.com/your-org/swift-route/actions"><img src="https://img.shields.io/github/workflow/status/your-org/swift-route/CI?label=build&style=flat-square" alt="Build Status"/></a>
</div>

---

# 🚀 swift‑route
**Power iOS/macOS developers with declarative, type‑safe routing for Swift applications.**  
A lightweight, zero‑dependency Swift package that lets you define navigation paths, URL patterns, and deep‑link handling in a single, compile‑time‑checked DSL.

## Why swift‑route? 🚀
- **Zero Runtime Overhead** — All routing logic is resolved at compile time; no reflection or string‑based look‑ups.
- **Type‑Safe Paths** — Compile‑time guarantees that every route’s parameters match the destination’s initializer.
- **Deep‑Link Ready** — One‑line registration of universal links and custom URL schemes.
- **Swift‑First** — Pure Swift implementation, no Objective‑C bridging required.
- **Modular Design** — Import only the core router or the optional UI helpers you need.
- **Test‑Friendly** — Routes are plain structs; unit‑test them with standard XCTest assertions.
- **Open‑Source Friendly** — MIT‑licensed, fully documented, and ready for community contributions.

## Feature Overview

| Feature | Description |
|---------|-------------|
| **Declarative DSL** | Define routes using a Swift DSL that mirrors your view hierarchy. |
| **Parameter Extraction** | Automatic parsing of path and query parameters into strongly‑typed structs. |
| **Deep‑Link Mapping** | Register universal links and custom schemes with a single API call. |
| **Navigation Helpers** | Extension methods for `UIViewController`, `SwiftUI.View`, and `NSViewController`. |
| **Route Guards** | Plug‑in based pre‑condition checks (e.g., auth, feature flags). |
| **Compile‑Time Validation** | Build fails if a route references a non‑existent view or mismatched parameters. |
| **Extensible Middleware** | Chainable interceptors for logging, analytics, or analytics. |

## Tech Stack
*No tech‑stack decisions have been locked yet.*  
(When the `decisions/tech-stack.md` file is populated, this section will be updated verbatim.)

## Project Structure

```
swift-route/
├─ business/          # Core routing engine and guard implementations
│   └─ *.swift
├─ docs/              # Design docs, PRD, ROADMAP, etc.
│   ├─ PRD.md
│   ├─ REQUIREMENTS.md
│   ├─ TECH_SPEC.md
│   ├─ BMC.md
│   ├─ STORIES.md
│   └─ ROADMAP.md
└─ Package.swift      # Swift Package Manager manifest
```

## Getting Started

```bash
# Clone the repository
git clone https://github.com/your-org/swift-route.git
cd swift-route

# Resolve Swift package dependencies (none required for the core)
swift package resolve

# Build the library
swift build -c release

# Run the test suite
swift test
```

### Adding to Your Project (Swift Package Manager)

```swift
// In your Package.swift
.package(url: "https://github.com/your-org/swift-route.git", from: "1.0.0")
```

```swift
// In your target dependencies
.target(
    name: "YourApp",
    dependencies: [
        .product(name: "SwiftRoute", package: "swift-route")
    ]
)
```

## Deploy

The library is distributed via the Swift Package Registry. After tagging a release, push the tag:

```bash
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions (defined in `.github/workflows/ci.yml`) will automatically publish the package metadata to the Swift Package Index.

## Status
Actively maintained – latest commit `096b06d` adds startup artifacts (PRD, REQUIREMENTS, TECH_SPEC, BMC, STORIES, ROADMAP).

## Contributing
Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to propose enhancements, report bugs, and submit pull requests.

## License
This project is licensed under the **MIT License**.