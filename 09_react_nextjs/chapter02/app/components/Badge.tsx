interface BadgeType {
    theme: string;
    children: React.ReactNode;
}

export default function Badge({
    theme,
    children,
}: BadgeType): React.JSX.Element {
    return (
        <span className={theme === 'dark' ? 'bg-pink-900' : 'bg-zinc-600'}>
            {children}
        </span>
    );
}
