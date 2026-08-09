import "./ContentHistory.css"

function SavedContent() {
  return (
    <div className="content-history">
      <div className="content-items">
        <div className="content-item"></div>
        <div className="content-item"></div>
        <div className="content-item"></div>
      </div>
      <svg style={{ display: 'none' }}>
        <defs>
          <filter id="displacementFilter">
            <feTurbulence type="turbulence" baseFrequency="0.01" numOctaves="2" result="turbulence" />
            <feDisplacementMap in="SourceGraphic" in2="displacementMap" xChannelSelector="R" yChannelSelector="G" scale="200" />
          </filter>
        </defs>
      </svg>
    </div>
  )
}

export default SavedContent
