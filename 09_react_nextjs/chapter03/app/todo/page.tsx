'use client';

import TodoItem from '@/domains/todo/components/TodoItem';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ChangeEvent, FormEvent, useState, useCallback } from 'react';
import Link from 'next/link';

export interface Todo {
    id?: number;
    title?: string;
    checked?: boolean;
}

const initialValue: Todo = {
    title: '',
    checked: false,
};

export default function TodoPage(): React.JSX.Element {
    const [form, setForm] = useState<Todo>(initialValue);
    const [items, setItems] = useState<Todo[]>([]);

    // const onChange = useCallback((e: ChangeEvent<HTMLInputElement>) => {
    //     setForm({ ...form, title: e.target.value });
    // }, [form]);
    // 두번째 매개변수 []는 함수가 새롭게 정의되는 기준 값을 설정. [] => 한 번 정의되면 다시 생성되지 않음
    // [form] -> form 객체가 변하면 useCallback에 정의된 함수가 새로 정의되고 생성된다

    const onChange = useCallback((e: ChangeEvent<HTMLInputElement>) => {
        setForm((prev) => ({ ...prev, title: e.target.value }));
    }, []);

    // const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    //     e.preventDefault();
    //     setItems(items.concat([{ ...form, id: Date.now() }]));
    //     // 등록 완료 이후 값 초기화
    //     setForm({ ...initialValue });
    // };

    const onSubmit = useCallback(
        (e: FormEvent<HTMLFormElement>) => {
            e.preventDefault();

            const newItems = { ...form, id: Date.now() };

            setItems((prev) => prev.concat(newItems));

            // 등록 완료 이후 값 초기화
            setForm({ ...initialValue });
        },
        [form],
    );

    const onClick = useCallback((id: number) => {
        setItems((prev) =>
            prev.map((item) =>
                item.id === id ? { ...item, checked: !item.checked } : item,
            ),
        );
    }, []);

    const onRemove = useCallback((id: number) => {
        setItems((prev) => prev.filter((item) => item.id !== id));
        // id와 일치하는 객체 삭제, 새로운 목록 생성
    }, []);

    return (
        <div>
            <form
                className="flex gap-1 justify-center mx-auto w-max-[450px] w-full"
                onSubmit={onSubmit}
            >
                <Input
                    type="text"
                    name="title"
                    className="border"
                    placeholder="write anything..."
                    onChange={onChange}
                    value={form.title}
                />
                <Button
                    variant="outline"
                    type="submit"
                    className="cursor-pointer"
                >
                    add
                </Button>
            </form>
            <ul>
                {items.length === 0 ? (
                    <li>nothing added yet</li>
                ) : (
                    items.map((item) => (
                        <TodoItem
                            key={item.id}
                            {...item}
                            onClick={onClick}
                            onRemove={onRemove}
                        />
                    ))
                )}
            </ul>
            <Link href="/login">
                login(CSR - SPA) fetch, 페이지 이동 없음, AJAX 기반, 한번
                다운받은 자원 재활용하므로 빠른 이동, DOM not loaded, using Link
            </Link>
            <br />
            <a href="/login">
                login(SSR - MPA) no fetch, re renders the page using A tag
            </a>
        </div>
    );
}
