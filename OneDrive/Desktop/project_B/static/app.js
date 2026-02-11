document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('skills-form')
  const outputEl = document.getElementById('output') || document.querySelector('.results-section')
  const summaryEl = document.getElementById('summary')
  const careersEl = document.getElementById('careers-container')

  form.addEventListener('submit', async (e) => {
    e.preventDefault()
    
    const checked = Array.from(form.querySelectorAll('input[name="skills"]:checked')).map(i => i.value)
    const skillLevel = form.querySelector('input[name="skillLevel"]:checked').value

    if (checked.length === 0) {
      alert('🎯 Please select at least one skill to get personalized recommendations!')
      return
    }

    // Show output section with animation
    outputEl.classList.remove('hidden')
    
    // Scroll to results
    setTimeout(() => {
      outputEl.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }, 100)

    // Update summary
    summaryEl.innerHTML = `
      ✨ Based on your <strong>${checked.join(', ')}</strong> skills at <strong>${skillLevel}</strong> level, here are your ideal career paths:
    `

    try {
      const res = await fetch('/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ skills: checked, skillLevel })
      })

      if (!res.ok) throw new Error('Failed to fetch recommendations')

      const data = await res.json()
      const recommendations = data.careers || []

      if (recommendations.length === 0) {
        careersEl.innerHTML = '<p style="grid-column: 1/-1; text-align: center; padding: 40px; color: #cbd5e1;">No matching careers found. Try selecting more skills!</p>'
        return
      }

      // Render career cards with staggered animation
      careersEl.innerHTML = recommendations.map((career, index) => `
        <div class="career-card" style="animation-delay: ${index * 0.1}s;">
          <h3>${career.name}</h3>
          <p class="career-desc">${career.description}</p>
          <div class="career-salary">💰 ${career.salary}</div>
          
          <div class="section-title">Learning Roadmap</div>
          <ul class="roadmap">
            ${(career.roadmap || []).map(step => `<li>${step}</li>`).join('')}
          </ul>
          
          <div class="section-title">Recommended Courses</div>
          <ul class="courses">
            ${(career.courses || []).map(course => `<li>${course}</li>`).join('')}
          </ul>
        </div>
      `).join('')
    } catch (err) {
      careersEl.innerHTML = '<p style="color: #ef4444; text-align: center; padding: 20px;">⚠️ Error: ' + err.message + '</p>'
    }
  })
})
