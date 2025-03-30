---
title: 'Open-Closed Principle in React: Building Extensible Components'
date: 2025-02-05
links:
  - https://cekrem.github.io/posts/open-closed-principle-in-react
tags:
  - react
---

✅ Do

```jsx
type ButtonBaseProps = {
  label: string;
  onClick: () => void;
  className?: string;
  children?: React.ReactNode;
};

const ButtonBase = ({
  label,
  onClick,
  className = "",
  children,
}: ButtonBaseProps) => (
  <button className={`button ${className}`.trim()} onClick={onClick}>
    {children || label}
  </button>
);

// Variant components extend the base
const PrimaryButton = (props: ButtonBaseProps) => (
  <ButtonBase {...props} className="button-primary" />
);

const SecondaryButton = (props: ButtonBaseProps) => (
  <ButtonBase {...props} className="button-secondary" />
);

const DangerButton = (props: ButtonBaseProps) => (
  <ButtonBase {...props} className="button-danger" />
);

Now we can easily add new variants without modifying existing code:

// Adding a new variant without touching the original components
const OutlineButton = (props: ButtonBaseProps) => (
  <ButtonBase {...props} className="button-outline" />
);
```

or

```jsx
type WithLoadingProps = {
  isLoading?: boolean;
};

const withLoading = <P extends object>(
  WrappedComponent: React.ComponentType<P>
) => {
  return ({ isLoading, ...props }: P & WithLoadingProps) => {
    if (isLoading) {
      return <div className="loader">Loading...</div>;
    }

    return <WrappedComponent {...(props as P)} />;
  };
};

// Usage
const UserProfileWithLoading = withLoading(UserProfile);
```

❌ Don't

```jsx
const Button = ({ label, onClick, variant }: ButtonProps) => {
  let className = 'button';

  // Direct modification for each variant
  if (variant === 'primary') {
    className += ' button-primary';
  } else if (variant === 'secondary') {
    className += ' button-secondary';
  } else if (variant === 'danger') {
    className += ' button-danger';
  }

  return (
    <button className={className} onClick={onClick}>
      {label}
    </button>
  );
};
```
