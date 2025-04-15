import { DocEvents } from "yjs/dist/src/internals";

export function createEscobarSplitButton(options: string[] = []): HTMLDivElement {
    //onst container = document.getElementById(containerId);
  
    const splitButton: HTMLDivElement = document.createElement('div');
    splitButton.className = 'escobar-split-button';
  
    const mainButton: HTMLButtonElement = document.createElement('button');
    mainButton.className = 'escobar-main-button';
    mainButton.textContent = options[0] || 'Select';
    //mainButton.onclick = () => alert(`Clicked: ${mainButton.textContent}`);
  
    const toggleButton: HTMLButtonElement = document.createElement('button');
    toggleButton.className = 'escobar-dropdown-toggle';
    
    // Create SVG icon for dropdown toggle
    const svgIcon = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svgIcon.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    svgIcon.setAttribute('width', '16');
    svgIcon.setAttribute('height', '16');
    svgIcon.setAttribute('viewBox', '0 0 24 24');
    svgIcon.setAttribute('fill', 'none');
    svgIcon.setAttribute('stroke', 'currentColor');
    svgIcon.setAttribute('stroke-width', '2');
    svgIcon.setAttribute('stroke-linecap', 'round');
    svgIcon.setAttribute('stroke-linejoin', 'round');
    svgIcon.classList.add('escobar-icon-svg');
    
    // Create path for chevron-down icon
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', 'M6 9l6 6 6-6');
    
    svgIcon.appendChild(path);
    toggleButton.appendChild(svgIcon);
  
    const dropdownMenu: HTMLUListElement = document.createElement('ul');
    dropdownMenu.className = 'escobar-dropdown-menu';
  
    options.forEach((option: string): void => {
      const li: HTMLLIElement = document.createElement('li');
      const btn: HTMLButtonElement = document.createElement('button');
      btn.textContent = option;
      btn.onclick = (e: MouseEvent): void => {
        e.stopPropagation(); // Prevent the document click handler from firing
        mainButton.textContent = option;
        dropdownMenu.style.display = 'none';
      };
      li.appendChild(btn);
      dropdownMenu.appendChild(li);
    });
  
    
    // Add click handler to document to close dropdown when clicking outside
    const closeDropdown = (e: MouseEvent): void => {
      if (dropdownMenu.style.display === 'block' && 
          !dropdownMenu.contains(e.target as Node) && 
          e.target !== toggleButton) {
        dropdownMenu.style.display = 'none';
      }
    };
    
    document.addEventListener('click', closeDropdown);
    
    toggleButton.onclick = (e: MouseEvent): void => {
      e.stopPropagation();
      
      // Simply toggle display
      if (dropdownMenu.style.display === 'block') {
        dropdownMenu.style.display = 'none';
      } else {
        // Remove from current parent if it exists
        if (dropdownMenu.parentNode) {
          dropdownMenu.parentNode.removeChild(dropdownMenu);
        }
        
        // Ensure the dropdown is appended to the body to avoid stacking context issues
        document.body.appendChild(dropdownMenu);
        
        // Get the button's position relative to the viewport
        const buttonRect = toggleButton.getBoundingClientRect();
        
        // Position it above the button
        dropdownMenu.style.position = 'fixed';
        dropdownMenu.style.bottom = `${window.innerHeight - buttonRect.top + 5}px`;
        dropdownMenu.style.right = `${window.innerWidth - buttonRect.right}px`;
        
        dropdownMenu.style.display = 'block';
      }
    };
    
    splitButton.appendChild(mainButton);
    splitButton.appendChild(toggleButton);
    splitButton.appendChild(dropdownMenu);
    
    splitButton["mainButton"] = mainButton;
    return splitButton;
  }
