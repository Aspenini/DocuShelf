# DocuShelf

**DocuShelf** is a macOS application built with Swift and SwiftUI that allows users to import, view, and manage PDF documents. The app provides a clean, organized way to display PDF thumbnails, select documents for detailed viewing, and manage an in-app library.

## Features

- **PDF Import**: Easily import PDF files to store in the app's local directory.
- **Thumbnail Grid View**: PDFs are displayed as thumbnails in a grid, making it easy to browse and select.
- **PDF Viewing**: Full-featured PDF viewer with page navigation.
- **File Management**: Store imported PDFs locally in the app’s directory for easy access.
- **macOS Compatibility**: Designed and optimized for macOS, with native UI components.

## Screenshots

![DocuShelf Thumbnail View](https://github.com/user-attachments/assets/c4416ae0-9fc7-4ff2-9b78-2cfe5ab94248)
![DocuShelf PDF Viewer](https://github.com/user-attachments/assets/b5e21087-c675-4c67-896e-237c1dc16051)

## Requirements

- macOS 12.0 or later
- Xcode 13.0 or later

## Installation

To run DocuShelf locally:

1. Clone the repository:
    ```bash
    git clone https://github.com/username/DocuShelf.git
    ```

2. Open the project in Xcode:
    ```bash
    cd DocuShelf
    open DocuShelf.xcodeproj
    ```

3. Build and run the project using Xcode.

## Usage

1. Launch the app.
2. Click on the **"+"** button to import a PDF file.
3. The imported PDFs are displayed as thumbnails in a grid layout.
4. Click on a PDF thumbnail to open it in the viewer.
5. Use the **Close** button to return to the thumbnail view.

## Project Structure

- **ContentView.swift**: Contains the main grid layout of PDF thumbnails and import functionality.
- **PDFViewer.swift**: Handles PDF viewing, including horizontal scrolling and scaling.
- **Document.swift**: Represents individual PDF documents and conforms to `Identifiable`.
- **FileManager Extensions**: Provides easy access to the app’s documents directory for local storage.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue to discuss new features or bugs.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Zip Foundation](https://github.com/weichsel/ZIPFoundation) - for handling zip compression (removed feature).
- [SwiftUI](https://developer.apple.com/documentation/swiftui/) - for the user interface components.
