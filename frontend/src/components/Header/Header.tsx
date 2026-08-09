import "./Header.css";
import { getUsername } from "../../utils/auth";
import { useState, useEffect } from "react";

function Header() {
  const [isScrolled, setIsScrolled] = useState(false);
  const username = getUsername() ?? "User";

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <header
      className={`section header-section ${isScrolled ? "is-scrolled" : ""}`}
    >
      <div className="brand-container">
        <p className="random-symbols">&gt; |</p>
        <img
          className="logo-img"
          src="https://res.cloudinary.com/diwkfbsgv/image/upload/v1775206748/logo_u4sz9t.svg"
        />
      </div>
      <div className="user-profile">
        <div className="user-content">
          <div className="user-details">
            <p className="user-role">Admin</p>
            <p className="user-name">{username}</p>
          </div>
          <div className="pfp-wrapper">
            <img
              src="https://res.cloudinary.com/diwkfbsgv/image/upload/v1786166423/copy_of_arkotype__tjx166.jpg"
              alt="pfp"
            />
          </div>
        </div>

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
                scale="200"
                xChannelSelector="R"
                yChannelSelector="G"
              />
            </filter>
          </defs>
        </svg>
      </div>
    </header>
  );
}

export default Header;
