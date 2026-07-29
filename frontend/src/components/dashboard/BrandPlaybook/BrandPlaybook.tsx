import "./BrandPlaybook.css";

// Props
import { CompanySelectionProps } from "../../../props";

// Modules
import { useState, useEffect } from "react";

function BrandPlaybook({ selectedCompany }: CompanySelectionProps) {
  const [screenWidth, setScreenWidth] = useState(window.innerWidth);
  const uploadInnerBorder = (
    <>
      <div className="pb-inner-border-path"></div>
      <div className="pb-inner-border"></div>
      <div className="pb-upload-prompt">
        <svg
          className="upload-icon"
          xmlns="http://www.w3.org/2000/svg"
          height="40px"
          viewBox="0 -960 960 960"
          width="40px"
          fill="currentColor"
        >
          <path d="M440-200h80v-167l64 64 56-57-160-160-160 160 57 56 63-63v167ZM240-80q-33 0-56.5-23.5T160-160v-640q0-33 23.5-56.5T240-880h320l240 240v480q0 33-23.5 56.5T720-80H240Zm280-520v-200H240v640h480v-440H520ZM240-800v200-200 640-640Z" />
        </svg>
        <div className="pb-upload-prompt-text">
          <span className="pb-upload-title">ADD PLAYBOOK</span>
          <p className="pb-upload-desc">Upload or drag and drop a PDF file</p>
        </div>
      </div>
    </>
  );

  useEffect(() => {
    const handleResize = () => setScreenWidth(window.innerWidth);
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  if (!selectedCompany) {
    return (
      <section className="brand-playbook component">
        <div className="section-title">
          <h2>+ BRAND PLAYBOOK</h2>
          <p className="random-symbols">////</p>
        </div>
        <div className="pb-container">
          {screenWidth <= 1100 ? (
            <div className="pb-summary" style={{ width: "100%" }}>
              <p style={{ width: "100%", padding: "2rem" }}>
                Select a company to view its playbook.
              </p>
            </div>
          ) : (
            <div className="pb-preview">
              <div className="pb-preview-options">
                <svg style={{ display: "none" }}>
                  <defs>
                    <filter id="displacementFilter">
                      <feTurbulence
                        type="turbulence"
                        baseFrequency="0.01"
                        numOctaves="2"
                        result="turbulence"
                      />
                      <feDisplacementMap
                        in="SourceGraphic"
                        in2="displacementMap"
                        xChannelSelector="R"
                        yChannelSelector="G"
                        scale="200"
                      />
                    </filter>
                  </defs>
                </svg>
              </div>
              <div className="pb-summary"></div>
            </div>
          )}
          <div className="pb-saved-content"></div>
          <div className="pb-upload-container">
            <div className="pb-upload-area">{uploadInnerBorder}</div>
            <div className="btn-primary">
              {screenWidth <= 1280 ? <p>Upload</p> : <p>Upload guidelines</p>}
              <svg
                className="arrow-outwards"
                xmlns="http://www.w3.org/2000/svg"
                height="48px"
                viewBox="0 -960 960 960"
                width="48px"
                fill="#D9D9D9"
              >
                <path d="m250-223-65-65 397-397H225v-91h512v511h-92v-355L250-223Z" />
              </svg>
              <svg style={{ display: "none" }}>
                <defs>
                  <filter id="displacementFilter">
                    <feTurbulence
                      type="turbulence"
                      baseFrequency="0.01"
                      numOctaves="2"
                      result="turbulence"
                    />
                    <feDisplacementMap
                      in="SourceGraphic"
                      in2="displacementMap"
                      xChannelSelector="R"
                      yChannelSelector="G"
                      scale="200"
                    />
                  </filter>
                </defs>
              </svg>
            </div>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="brand-playbook component">
      <div className="section-title">
        <h2>+ BRAND PLAYBOOK</h2>
        <p className="random-symbols">////</p>
      </div>
      <div className="pb-container">
        <div className="pb-preview">
          <div className="pb-preview-options">
            <p>o</p>
            <p>o</p>
            <p>o</p>
            <svg style={{ display: "none" }}>
              <defs>
                <filter id="displacementFilter">
                  <feTurbulence
                    type="turbulence"
                    baseFrequency="0.01"
                    numOctaves="2"
                    result="turbulence"
                  />
                  <feDisplacementMap
                    in="SourceGraphic"
                    in2="displacementMap"
                    xChannelSelector="R"
                    yChannelSelector="G"
                    scale="200"
                  />
                </filter>
              </defs>
            </svg>
          </div>
          <div className="pb-summary">
            <div className="pb-summary-header">
              <h1>{selectedCompany.name}</h1>
              <h2>{selectedCompany.industry.toUpperCase()}</h2>
            </div>
            <div>
              <div className="pb-description">
                <p className="category-content">
                  {selectedCompany.description}
                </p>
              </div>
              <div className="categories">
                <div className="category">
                  <p className="category-title">Tone</p>
                  <p className="category-content tone-content">
                    {selectedCompany.tone}
                  </p>
                </div>
                <div className="category">
                  <p className="category-title">Color palette</p>
                  <div className="pantones">
                    {selectedCompany.color_palette.map((color, index) => (
                      <div
                        key={index}
                        className="pantone"
                        style={{ backgroundColor: color }}
                      ></div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="pb-saved-content">
          <svg style={{ display: "none" }}>
            <defs>
              <filter id="displacementFilter">
                <feTurbulence
                  type="turbulence"
                  baseFrequency="0.01"
                  numOctaves="2"
                  result="turbulence"
                />
                <feDisplacementMap
                  in="SourceGraphic"
                  in2="displacementMap"
                  xChannelSelector="R"
                  yChannelSelector="G"
                  scale="200"
                />
              </filter>
            </defs>
          </svg>
        </div>
        <div className="pb-upload-container">
          <div className="pb-upload-area">{uploadInnerBorder}</div>
          <div className="btn-primary">
            {screenWidth <= 1280 ? <p>Upload</p> : <p>Upload guidelines</p>}
            <svg
              className="arrow-outwards"
              xmlns="http://www.w3.org/2000/svg"
              height="48px"
              viewBox="0 -960 960 960"
              width="48px"
              fill="#D9D9D9"
            >
              <path d="m250-223-65-65 397-397H225v-91h512v511h-92v-355L250-223Z" />
            </svg>
            <svg style={{ display: "none" }}>
              <defs>
                <filter id="displacementFilter">
                  <feTurbulence
                    type="turbulence"
                    baseFrequency="0.01"
                    numOctaves="2"
                    result="turbulence"
                  />
                  <feDisplacementMap
                    in="SourceGraphic"
                    in2="displacementMap"
                    xChannelSelector="R"
                    yChannelSelector="G"
                    scale="200"
                  />
                </filter>
              </defs>
            </svg>
          </div>
        </div>
      </div>
    </section>
  );
}

export default BrandPlaybook;
