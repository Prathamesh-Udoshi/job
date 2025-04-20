// Helper to create elements with classes and attributes
function createElement(type, options = {}) {
  const el = document.createElement(type);
  if (options.className) el.className = options.className;
  if (options.placeholder) el.placeholder = options.placeholder;
  if (options.type) el.type = options.type;
  if (options.title) el.title = options.title;
  if (options.textContent) el.textContent = options.textContent;
  if (options.value) el.value = options.value;
  return el;
}

// On resume.html - handle dynamic form inputs and submit
if (document.getElementById('resumeForm')) {
  const form = document.getElementById('resumeForm');

  // Photo preview
  const photoInput = document.getElementById('photo');
  const photoPreview = document.getElementById('photoPreview');

  photoInput.addEventListener('change', () => {
    const file = photoInput.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        photoPreview.style.backgroundImage = `url(${reader.result})`;
      };
      reader.readAsDataURL(file);
    } else {
      photoPreview.style.backgroundImage = '';
    }
  });

  // Skills dynamic inputs
  const skillsInputs = document.getElementById('skillsInputs');
  const addSkillBtn = document.getElementById('addSkillBtn');

  addSkillBtn.onclick = () => {
    const input = createElement('input', { type: 'text', className: 'skill-input', placeholder: 'Enter a skill' });
    skillsInputs.appendChild(input);
    input.focus();
  };

  // Education dynamic inputs
  const educationInputs = document.getElementById('educationInputs');
  const addEducationBtn = document.getElementById('addEducationBtn');

  addEducationBtn.onclick = () => {
    const entry = createElement('div', { className: 'education-entry' });

    const degreeInput = createElement('input', { type: 'text', className: 'degree-input', placeholder: 'Degree (e.g. B.Sc Computer Science)' });
    const dateInput = createElement('input', { type: 'text', className: 'edu-date-input', placeholder: 'Date (e.g. 2018 - 2022)' });
    const removeBtn = createElement('button', { className: 'remove-btn', title: 'Remove Education', textContent: '×' });

    removeBtn.onclick = () => {
      educationInputs.removeChild(entry);
    };

    entry.appendChild(degreeInput);
    entry.appendChild(dateInput);
    entry.appendChild(removeBtn);
    educationInputs.appendChild(entry);
    degreeInput.focus();
  };

  // Remove button for initial education entry
  educationInputs.querySelectorAll('.remove-btn').forEach(btn => {
    btn.onclick = () => {
      btn.parentElement.remove();
    };
  });

  // Experiences dynamic inputs
  const experienceInputs = document.getElementById('experienceInputs');
  const addExperienceBtn = document.getElementById('addExperienceBtn');

  addExperienceBtn.onclick = () => {
    const container = createElement('div', { className: 'experience-entry' });
    const textarea = createElement('textarea', { className: 'experience-input', placeholder: 'Describe an experience' });
    const removeBtn = createElement('button', { className: 'remove-btn', title: 'Remove Experience', textContent: '×' });

    removeBtn.onclick = () => {
      experienceInputs.removeChild(container);
    };

    container.appendChild(textarea);
    container.appendChild(removeBtn);
    experienceInputs.appendChild(container);
    textarea.focus();
  };

  // Remove button for initial experience entry
  experienceInputs.querySelectorAll('.remove-btn').forEach(btn => {
    btn.onclick = () => {
      btn.parentElement.remove();
    };
  });

  // Form submit
  form.addEventListener('submit', function (e) {
    e.preventDefault();

    // Get photo as base64
    const photoFile = photoInput.files[0];
    const bio = document.getElementById('bio').value.trim();

    // Collect skills
    const skills = Array.from(document.querySelectorAll('.skill-input'))
      .map(input => input.value.trim())
      .filter(s => s.length > 0);

    // Collect education entries
    const education = Array.from(document.querySelectorAll('.education-entry')).map(entry => {
      const degree = entry.querySelector('.degree-input').value.trim();
      const date = entry.querySelector('.edu-date-input').value.trim();
      return { degree, date };
    }).filter(e => e.degree.length > 0 || e.date.length > 0);

    const interests = document.getElementById('interests').value.trim();
    const projects = document.getElementById('projects').value.trim();

    // Collect experiences
    const experiences = Array.from(document.querySelectorAll('.experience-input'))
      .map(textarea => textarea.value.trim())
      .filter(e => e.length > 0);

    function saveAndRedirect(photoData) {
      const data = {
        photo: photoData || '',
        bio,
        skills,
        education,
        interests,
        projects,
        experiences,
      };
      localStorage.setItem('resumeData', JSON.stringify(data));
      window.location.href = '/generate';
      
    }
    

    if (photoFile) {
      const reader = new FileReader();
      reader.onload = () => saveAndRedirect(reader.result);
      reader.readAsDataURL(photoFile);
    } else {
      saveAndRedirect('');
    }
  });
}

// On generate.html - display resume and enable PDF download
if (document.getElementById('resumeContainer')) {
  const resumeData = JSON.parse(localStorage.getItem('resumeData') || '{}');
  const container = document.getElementById('resumeContainer');

  if (!resumeData || Object.keys(resumeData).length === 0) {
    container.innerHTML = '<p>No resume data found. Please build your resume first.</p>';
  } else {
    // Build HTML for skills list
    const skillsHTML = resumeData.skills && resumeData.skills.length
      ? `<ul class="skills-list">${resumeData.skills.map(s => `<li>${s}</li>`).join('')}</ul>`
      : '<p>N/A</p>';

    // Build HTML for education list
    const educationHTML = resumeData.education && resumeData.education.length
      ? `<ul class="education-list">${resumeData.education.map(e => `
          <li>
            <strong>${e.degree || 'N/A'}</strong>
            ${e.date ? `<span class="date">${e.date}</span>` : ''}
          </li>`).join('')}</ul>`
      : '<p>N/A</p>';

    // Build HTML for projects list (comma separated)
    const projectsHTML = resumeData.projects
      ? `<ul class="projects-list">${resumeData.projects.split(',').map(p => `<li>${p.trim()}</li>`).join('')}</ul>`
      : '<p>N/A</p>';

    // Build HTML for experiences list
    const experiencesHTML = resumeData.experiences && resumeData.experiences.length
      ? `<ul class="experience-list">${resumeData.experiences.map(e => `<li>${e}</li>`).join('')}</ul>`
      : '<p>N/A</p>';

    container.innerHTML = `
      <div class="left">
        ${resumeData.photo ? `<img src="${resumeData.photo}" alt="Your Photo" />` : ''}
        <section>
          <h2>Personal Bio</h2>
          <p>${resumeData.bio || 'N/A'}</p>
        </section>
        <section>
          <h2>Skills</h2>
          ${skillsHTML}
        </section>
      </div>
      <div class="right">
        <section>
          <h2>Education</h2>
          ${educationHTML}
        </section>
        <section>
          <h2>Interests</h2>
          <p>${resumeData.interests || 'N/A'}</p>
        </section>
        <section>
          <h2>Projects</h2>
          ${projectsHTML}
        </section>
        <section>
          <h2>Experiences</h2>
          ${experiencesHTML}
        </section>
      </div>
    `;
  }

  // PDF download button
  const downloadBtn = document.getElementById('downloadPdfBtn');
  downloadBtn.onclick = () => {
    if (!resumeData || Object.keys(resumeData).length === 0) {
      alert('No resume data to download!');
      return;
    }
    generatePDF(resumeData);
  };

  function generatePDF(data) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF('p', 'pt', 'a4');
    const margin = 40;
    const pageWidth = doc.internal.pageSize.width;
    let y = margin;

    // Add photo centered circle
    if (data.photo) {
      doc.addImage(data.photo, 'JPEG', (pageWidth / 2) - 50, y, 100, 100);
      y += 110;
    }

    // Personal Bio
    doc.setFontSize(18);
    doc.setTextColor('#4a90e2');
    doc.setFont('helvetica', 'bold');
    doc.text('Personal Bio', margin, y);
    y += 24;
    doc.setFontSize(12);
    doc.setTextColor('#222');
    doc.setFont('helvetica', 'normal');
    doc.text(doc.splitTextToSize(data.bio || 'N/A', pageWidth - margin * 2), margin, y);
    y += 70;

    // Two column layout
    const leftX = margin;
    const rightX = pageWidth / 2 + 10;
    let leftY = y;
    let rightY = y;

    // Skills (left)
    doc.setFontSize(16);
    doc.setTextColor('#4a90e2');
    doc.setFont('helvetica', 'bold');
    doc.text('Skills', leftX, leftY);
    leftY += 22;
    doc.setFontSize(12);
    doc.setTextColor('#222');
    doc.setFont('helvetica', 'normal');
    if (data.skills && data.skills.length) {
      data.skills.forEach(skill => {
        doc.text(`• ${skill}`, leftX + 10, leftY);
        leftY += 18;
      });
    } else {
      doc.text('N/A', leftX + 10, leftY);
      leftY += 18;
    }
    leftY += 20;

    // Education (right)
    doc.setFontSize(16);
    doc.setTextColor('#4a90e2');
    doc.setFont('helvetica', 'bold');
    doc.text('Education', rightX, rightY);
    rightY += 22;
    doc.setFontSize(12);
    doc.setTextColor('#222');
    doc.setFont('helvetica', 'normal');
    if (data.education && data.education.length) {
      data.education.forEach(edu => {
        doc.text(edu.degree || 'N/A', rightX + 10, rightY);
        rightY += 16;
        if (edu.date) {
          doc.setFontSize(10);
          doc.setTextColor('#666');
          doc.text(edu.date, rightX + 10, rightY);
          doc.setFontSize(12);
          doc.setTextColor('#222');
          rightY += 18;
        } else {
          rightY += 10;
        }
      });
    } else {
      doc.text('N/A', rightX + 10, rightY);
      rightY += 18;
    }
    rightY += 20;

    // Interests (left)
    doc.setFontSize(16);
    doc.setTextColor('#4a90e2');
    doc.setFont('helvetica', 'bold');
    doc.text('Interests', leftX, leftY);
    leftY += 22;
    doc.setFontSize(12);
    doc.setTextColor('#222');
    doc.setFont('helvetica', 'normal');
    doc.text(doc.splitTextToSize(data.interests || 'N/A', (pageWidth / 2) - margin - 20), leftX, leftY);
    leftY += 50;

    // Projects (right)
    doc.setFontSize(16);
    doc.setTextColor('#4a90e2');
    doc.setFont('helvetica', 'bold');
    doc.text('Projects', rightX, rightY);
    rightY += 22;
    doc.setFontSize(12);
    doc.setTextColor('#222');
    doc.setFont('helvetica', 'normal');
    if (data.projects) {
      const projects = data.projects.split(',').map(p => p.trim());
      projects.forEach(proj => {
        doc.text(`• ${proj}`, rightX + 10, rightY);
        rightY += 18;
      });
    } else {
      doc.text('N/A', rightX + 10, rightY);
      rightY += 18;
    }
    rightY += 20;

    // Experiences (left)
    doc.setFontSize(16);
    doc.setTextColor('#4a90e2');
    doc.setFont('helvetica', 'bold');
    doc.text('Experiences', leftX, leftY);
    leftY += 22;
    doc.setFontSize(12);
    doc.setTextColor('#222');
    doc.setFont('helvetica', 'normal');
    if (data.experiences && data.experiences.length) {
      data.experiences.forEach(exp => {
        const lines = doc.splitTextToSize(exp, (pageWidth / 2) - margin - 20);
        doc.text(lines, leftX, leftY);
        leftY += lines.length * 16 + 10;
      });
    } else {
      doc.text('N/A', leftX, leftY);
      leftY += 18;
    }

    doc.save('resume.pdf');
  }
}