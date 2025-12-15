import { Box, Flex, IconButton } from "@chakra-ui/react";
import { Document, Page, pdfjs } from "react-pdf";
import { useState, useRef, useEffect } from "react";
import pdfWorker from "pdfjs-dist/build/pdf.worker.min.mjs?url";

import Openinnewwindow from "./Openinnewwindow"

import { CiZoomIn } from "react-icons/ci";
import { CiZoomOut } from "react-icons/ci";
import { TbZoomReset } from "react-icons/tb";
pdfjs.GlobalWorkerOptions.workerSrc = pdfWorker;

const PdfViewer = ({ fileUrl, page }: { fileUrl: string; page: number }) => {
  const [numPages, setNumPages] = useState<number | null>(null);
  const [scale, setScale] = useState(1.1);
  const [containerWidth, setContainerWidth] = useState<number>(0);
  const containerRef = useRef<HTMLDivElement>(null);
  const onLoadSuccess = ({ numPages }: { numPages: number }) => {
    setNumPages(numPages);
  };

  useEffect(() => {
    if (!containerRef.current) return;
    console.log(numPages);
    const observer = new ResizeObserver(entries => {
      for (let entry of entries) {
        setContainerWidth(entry.contentRect.width);
      }
    });

    observer.observe(containerRef.current);
    return () => observer.disconnect();
  }, []);
  return (
    <Flex direction="column" ref={containerRef} h="100%" overflowY="auto" alignItems={'center'}>
      <Flex justify="flex-end" gap={2} p={2}>
        <Openinnewwindow pdfUrl={fileUrl} page={page} />
        <IconButton
          aria-label="Zoom out"
          size="sm"
          onClick={() => setScale(s => Math.max(s - 0.2, 0.6))}
        ><CiZoomOut /></IconButton>
        <IconButton
          aria-label="Reset zoom"
          size="sm"
          onClick={() => setScale(1.0)}
        ><TbZoomReset /></IconButton>
        <IconButton
          aria-label="Zoom in"
          size="sm"
          onClick={() => setScale(s => Math.min(s + 0.2, 3))}
        ><CiZoomIn /></IconButton>
      </Flex>
      <Box
        w="100%"
        minW="300px"
        h="100vh"
        p={2}
        resize="horizontal"
      >
        <Document file={fileUrl} onLoadSuccess={onLoadSuccess}>
          <Page
            pageNumber={page}
            width={containerWidth ? containerWidth * scale : undefined}
            renderTextLayer={false}
            renderAnnotationLayer={false}
          />
        </Document>
      </Box>
    </Flex>
  );
};

export default PdfViewer;
