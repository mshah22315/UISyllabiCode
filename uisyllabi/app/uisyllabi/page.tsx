import { createClient } from '@/utils/supabase/server'

export default async function Page() {
  const supabase = await createClient()
  const { data: courses } = await supabase.from('coursesv2').select()

  return <pre>{JSON.stringify(courses, null, 2)}</pre>
}