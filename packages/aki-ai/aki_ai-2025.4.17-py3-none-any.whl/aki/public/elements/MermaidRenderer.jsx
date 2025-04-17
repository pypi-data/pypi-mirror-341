import { useEffect, useRef, useState } from 'react';

export default function MermaidRenderer() {
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [error, setError] = useState(null);
  const containerRef = useRef(null);
  const fullscreenRef = useRef(null);

  // CSS styles similar to the user script
  const styles = {
    container: {
      margin: '20px 0',
      padding: '15px',
      borderRadius: '8px',
      backgroundColor: '#f9f9f9',
      boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
      position: 'relative',
      fontFamily: "'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif"
    },
    mermaid: {
      width: '100%'
    },
    svg: {
      maxWidth: '100%',
      height: 'auto !important',
      display: 'block',
      margin: '0 auto'
    },
    error: {
      color: '#e74c3c',
      padding: '10px',
      textAlign: 'center',
      fontFamily: 'sans-serif',
      fontSize: '14px'
    },
    fullscreenBtn: {
      position: 'absolute',
      top: '10px',
      right: '10px',
      backgroundColor: 'rgba(41, 128, 185, 0.7)',
      color: 'white',
      border: 'none',
      padding: '5px 8px',
      borderRadius: '4px',
      fontSize: '10px',
      cursor: 'pointer',
      opacity: 0,
      transition: 'opacity 0.3s ease',
      zIndex: 100
    },
    fullscreenOverlay: {
      position: 'fixed',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      backgroundColor: 'rgba(0, 0, 0, 0.85)',
      zIndex: 10000,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px',
      boxSizing: 'border-box'
    },
    fullscreenContent: {
      width: '90%',
      height: '90%',
      backgroundColor: 'white',
      borderRadius: '8px',
      padding: '20px',
      boxSizing: 'border-box',
      position: 'relative',
      overflow: 'auto',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center'
    },
    fullscreenClose: {
      position: 'absolute',
      top: '10px',
      right: '10px',
      backgroundColor: '#e74c3c',
      color: 'white',
      border: 'none',
      padding: '5px 12px',
      borderRadius: '4px',
      fontSize: '14px',
      cursor: 'pointer',
      zIndex: 10001
    },
    fullscreenMermaid: {
      width: '100%',
      height: '100%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    },
    fullscreenSvg: {
      maxWidth: '95% !important',
      maxHeight: '90% !important',
      height: 'auto !important'
    }
  };

  // Initialize mermaid when the component mounts
  useEffect(() => {
    loadMermaid();
  }, []);

  // Function to load mermaid library if not already loaded
  const loadMermaid = () => {
    if (window.mermaid) {
      initMermaid();
      return;
    }

    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js';
    script.async = true;
    script.onload = () => {
      console.log('Mermaid script loaded');
      initMermaid();
    };
    script.onerror = (e) => {
      console.error('Failed to load mermaid script:', e);
      setError('Failed to load mermaid library');
    };
    document.body.appendChild(script);
  };

  // Initialize mermaid with settings matching the user script
  const initMermaid = () => {
    if (!window.mermaid) return;

    window.mermaid.initialize({
      startOnLoad: false,
      theme: 'default',
      securityLevel: 'loose',
      fontFamily: 'Trebuchet MS, Lucida Sans Unicode, Lucida Grande, Lucida Sans, Arial, sans-serif',
      logLevel: 'fatal', // Reduce console logging
      flowchart: {
        htmlLabels: true,
        curve: 'linear'
      }
    });

    renderDiagram();
  };

  // Function to render the diagram
  const renderDiagram = () => {
    if (!containerRef.current || !window.mermaid) return;

    // Access mermaid code from global variable if it exists
    const mermaidCode = window.mermaidCode || 
                     (window.props && window.props.mermaidCode) || 
                     (typeof props !== 'undefined' && props && props.mermaidCode);

    if (!mermaidCode) {
      setError('No mermaid code found. Please check component implementation.');
      return;
    }

    try {
      // Create a unique ID for this diagram
      const id = 'mermaid-' + Date.now() + '-' + Math.floor(Math.random() * 1000);
      
      // Parse and render the diagram
      window.mermaid.parse(mermaidCode)
        .then(() => {
          return window.mermaid.render(id, mermaidCode);
        })
        .then(result => {
          // Create a diagram container to display the result
          containerRef.current.innerHTML = result.svg;
          
          // Store the original code as a data attribute
          containerRef.current.setAttribute('data-mermaid-code', mermaidCode);
          
          // Apply styling to the SVG
          const svg = containerRef.current.querySelector('svg');
          if (svg) {
            svg.style.maxWidth = '100%';
            svg.style.height = 'auto';
            svg.style.maxHeight = '700px'; // Prevent excessive vertical scaling
            svg.style.display = 'block';
            svg.style.margin = '0 auto';
            // Ensure proper aspect ratio
            svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
          }
        })
        .catch(err => {
          console.error('Mermaid rendering error:', err);
          setError(`Diagram rendering error: ${err.message}`);
        });
    } catch (err) {
      console.error('Mermaid rendering error:', err);
      setError(`Diagram rendering error: ${err.message}`);
    }
  };

  // Function to toggle fullscreen mode
  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
    
    // When entering fullscreen, render the diagram in the fullscreen container
    if (!isFullscreen && containerRef.current) {
      const mermaidCode = containerRef.current.getAttribute('data-mermaid-code');
      if (mermaidCode) {
        setTimeout(() => {
          if (fullscreenRef.current && window.mermaid) {
            const id = 'mermaid-fullscreen-' + Date.now();
            window.mermaid.render(id, mermaidCode)
              .then(result => {
                fullscreenRef.current.innerHTML = result.svg;
                
                // Apply fullscreen-specific styling
                const svg = fullscreenRef.current.querySelector('svg');
                if (svg) {
                  svg.style.maxWidth = '95%';
                  svg.style.maxHeight = '90%';
                  svg.style.height = 'auto';
                  // Ensure proper aspect ratio
                  svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
                }
              })
              .catch(err => {
                console.error('Fullscreen rendering error:', err);
                if (fullscreenRef.current) {
                  fullscreenRef.current.innerHTML = `<div style="color: #e74c3c; padding: 10px; text-align: center;">Fullscreen rendering failed</div>`;
                }
              });
          }
        }, 100);
      }
    }
  };

  // Handle ESC key to exit fullscreen
  useEffect(() => {
    const handleEscKey = (event) => {
      if (isFullscreen && event.key === 'Escape') {
        setIsFullscreen(false);
      }
    };

    document.addEventListener('keydown', handleEscKey);
    return () => {
      document.removeEventListener('keydown', handleEscKey);
    };
  }, [isFullscreen]);

  // Handle hover effect for fullscreen button
  useEffect(() => {
    if (!containerRef.current) return;

    const container = containerRef.current.closest('.mermaid-container');
    const btn = container?.querySelector('.fullscreen-btn');
    
    if (container && btn) {
      const handleMouseOver = () => {
        btn.style.opacity = '1';
      };
      
      const handleMouseOut = () => {
        btn.style.opacity = '0';
      };
      
      container.addEventListener('mouseover', handleMouseOver);
      container.addEventListener('mouseout', handleMouseOut);
      
      return () => {
        container.removeEventListener('mouseover', handleMouseOver);
        container.removeEventListener('mouseout', handleMouseOut);
      };
    }
  }, []);

  return (
    <>
      <div className="mermaid-container" style={styles.container}>
        {/* Fullscreen button */}
        <button 
          className="fullscreen-btn"
          style={styles.fullscreenBtn}
          onClick={toggleFullscreen}
          title="View diagram in fullscreen mode"
        >
          Fullscreen
        </button>
        
        {/* Mermaid diagram container */}
        <div className="mermaid" style={styles.mermaid} ref={containerRef}></div>
        
        {/* Error message if rendering fails */}
        {error && <div style={styles.error}>{error}</div>}
      </div>
      
      {/* Fullscreen overlay */}
      {isFullscreen && (
        <div style={styles.fullscreenOverlay}>
          <div style={styles.fullscreenContent}>
            <button 
              style={styles.fullscreenClose} 
              onClick={toggleFullscreen}
            >
              Close
            </button>
            <div className="mermaid" style={styles.fullscreenMermaid} ref={fullscreenRef}></div>
          </div>
        </div>
      )}
    </>
  );
}