//
//  PDFViewer.swift
//  DocuShelf
//
//  Created by Aspen Carter Feltner on 11/2/24.
//


import SwiftUI
import PDFKit

struct PDFViewer: NSViewRepresentable {
    let url: URL
    var onClose: () -> Void

    func makeNSView(context: Context) -> NSView {
        let pdfView = PDFView()
        pdfView.autoScales = true
        pdfView.displayMode = .singlePageContinuous
        pdfView.displayDirection = .horizontal
        pdfView.document = PDFDocument(url: url)

        // Wrap PDFView in a NSStackView to add the close button
        let stackView = NSStackView()
        stackView.orientation = .vertical
        stackView.spacing = 10

        let closeButton = NSButton(title: "Close", target: context.coordinator, action: #selector(Coordinator.close))
        closeButton.bezelStyle = .rounded
        closeButton.setFrameSize(NSSize(width: 60, height: 30))
        
        stackView.addArrangedSubview(closeButton)
        stackView.addArrangedSubview(pdfView)
        
        return stackView
    }

    func updateNSView(_ nsView: NSView, context: Context) {}

    func makeCoordinator() -> Coordinator {
        Coordinator(onClose: onClose)
    }

    class Coordinator: NSObject {
        var onClose: () -> Void

        init(onClose: @escaping () -> Void) {
            self.onClose = onClose
        }

        @objc func close() {
            onClose()
        }
    }
}
