export default function ProgressBar({ currentStep }) {
  const steps = [
    { id: 'login', label: 'Login', description: 'Accede con tu email' },
    { id: 'onboarding', label: 'Perfil', description: 'Define tu contexto' },
    { id: 'dashboard', label: 'Dashboard', description: 'Gestiona decisiones' }
  ];

  const currentIndex = steps.findIndex(s => s.id === currentStep);

  return (
    <div style={{
      backgroundColor: '#f9f9f9',
      padding: '20px',
      marginBottom: '20px',
      borderRadius: '8px',
      borderLeft: '4px solid #4285f4'
    }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        position: 'relative'
      }}>
        {/* Progress line */}
        <div style={{
          position: 'absolute',
          top: '20px',
          left: '0',
          right: '0',
          height: '2px',
          backgroundColor: '#e0e0e0',
          zIndex: 1
        }}>
          <div style={{
            height: '100%',
            backgroundColor: '#4285f4',
            width: `${currentIndex * 50}%`,
            transition: 'width 0.3s'
          }} />
        </div>

        {/* Steps */}
        {steps.map((step, index) => {
          const isActive = index <= currentIndex;
          const isCurrent = index === currentIndex;

          return (
            <div
              key={step.id}
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                flex: 1,
                zIndex: 2,
                position: 'relative'
              }}
            >
              {/* Circle */}
              <div
                style={{
                  width: '40px',
                  height: '40px',
                  borderRadius: '50%',
                  backgroundColor: isActive ? '#4285f4' : '#e0e0e0',
                  color: isActive ? 'white' : '#999',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 'bold',
                  marginBottom: '8px',
                  transition: 'all 0.3s',
                  boxShadow: isCurrent ? '0 0 0 4px rgba(66, 133, 244, 0.2)' : 'none'
                }}
              >
                {index + 1}
              </div>

              {/* Label */}
              <div
                style={{
                  textAlign: 'center',
                  fontSize: '14px',
                  fontWeight: isCurrent ? 'bold' : 'normal',
                  color: isCurrent ? '#4285f4' : '#666'
                }}
              >
                {step.label}
              </div>
              <div
                style={{
                  textAlign: 'center',
                  fontSize: '12px',
                  color: '#999',
                  marginTop: '4px',
                  maxWidth: '100px'
                }}
              >
                {step.description}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
