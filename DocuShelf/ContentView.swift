import SwiftUI
import PDFKit
import UniformTypeIdentifiers

struct ContentView: View {
    @State private var documents: [Document] = []
    @State private var selectedDocument: Document?

    var body: some View {
        VStack {
            ScrollView {
                LazyVGrid(columns: [GridItem(.adaptive(minimum: 150))], spacing: 20) {
                    ForEach(documents) { document in
                        Button(action: {
                            selectedDocument = document
                        }) {
                            PDFThumbnail(url: document.url)
                        }
                        .buttonStyle(PlainButtonStyle())
                    }
                }
                .padding()
            }
            .onAppear(perform: loadDocuments)
            .toolbar {
                ToolbarItem {
                    Button(action: openDocumentPicker) {
                        Image(systemName: "plus")
                            .font(.title2)
                    }
                }
            }
        }
        .sheet(item: $selectedDocument) { document in
            PDFViewer(url: document.url) {
                selectedDocument = nil // Close button action
            }
            .frame(minWidth: 800, minHeight: 600) // Larger view for PDF viewer
        }
        .frame(minWidth: 900, minHeight: 700) // Larger default window size
    }

    private func openDocumentPicker() {
        let panel = NSOpenPanel()
        panel.allowedContentTypes = [.pdf]
        panel.allowsMultipleSelection = false
        panel.canChooseDirectories = false

        if panel.runModal() == .OK, let selectedURL = panel.url {
            let destinationURL = FileManager.default.documentsDirectory.appendingPathComponent(selectedURL.lastPathComponent)
            do {
                if !FileManager.default.fileExists(atPath: destinationURL.path) {
                    try FileManager.default.copyItem(at: selectedURL, to: destinationURL)
                    documents.append(Document(url: destinationURL))
                }
            } catch {
                print("Failed to import file: \(error)")
            }
        }
    }

    private func loadDocuments() {
        let documentsDirectory = FileManager.default.documentsDirectory
        do {
            documents = try FileManager.default.contentsOfDirectory(at: documentsDirectory, includingPropertiesForKeys: nil)
                .filter { $0.pathExtension == "pdf" }
                .map { Document(url: $0) }
        } catch {
            print("Failed to load documents: \(error)")
        }
    }
}

// Document struct to conform to Identifiable protocol
struct Document: Identifiable {
    let id = UUID()
    let url: URL
}

// Thumbnail view for displaying the PDF cover
struct PDFThumbnail: View {
    let url: URL

    var body: some View {
        if let pdfDocument = PDFDocument(url: url),
           let pdfPage = pdfDocument.page(at: 0) {
            let pdfThumbnail = pdfPage.thumbnail(of: CGSize(width: 150, height: 200), for: .cropBox)
            Image(nsImage: pdfThumbnail)
                .resizable()
                .aspectRatio(contentMode: .fit)
                .frame(width: 150, height: 200)
                .cornerRadius(8)
                .shadow(radius: 4)
        } else {
            Rectangle()
                .fill(Color.gray)
                .frame(width: 150, height: 200)
                .cornerRadius(8)
        }
    }
}

// Extension for FileManager to access the app's Documents directory
extension FileManager {
    var documentsDirectory: URL {
        urls(for: .documentDirectory, in: .userDomainMask)[0]
    }
}

