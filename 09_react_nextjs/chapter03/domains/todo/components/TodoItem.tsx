import { type Todo } from '@/app/todo/page';
import { WiAlien } from 'react-icons/wi';
import { IoAccessibilityOutline } from 'react-icons/io5';
import { LuTrash2 } from 'react-icons/lu';

type TodoItemProps = Todo & {
    onClick: (id?: number) => void;
    onRemove: (id?: number) => void;
};

export default function TodoItem({
    id,
    title,
    checked,
    onClick,
    onRemove,
}: TodoItemProps): React.JSX.Element {
    return (
        <li className="flex">
            <div
                className="flex"
                onClick={() => {
                    onClick(id!);
                }}
            >
                {checked ? <WiAlien /> : <IoAccessibilityOutline />}
                {title}
            </div>
            <span>
                <LuTrash2
                    onClick={() => {
                        onRemove(id!);
                    }}
                />
            </span>
        </li>
    );
}

//export default React.memo(TodoItem);
