from langchain_openai import AzureChatOpenAI

def check_article_structure(llm: AzureChatOpenAI, text: str) -> str:  
    """Check the structure of the article based on predefined rules."""  

    prompt = f"""
    <EvaluationRequest>
        <Role>
            You are a <strong>web content evaluation expert</strong> with professional experience in optimizing article structures.
        </Role>

        <Mission>
            <Overview>
                Your mission is to <strong>check and evaluate the structure of the article</strong> based on technical and academic criteria.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Check the main components</Title>
                    <Details>
                        <Point>Title: Is it appropriately long and does it accurately reflect the content of the article?</Point>
                        <Point>Summary (Key Insights): Does it briefly describe the problem, insights, and results of the article?</Point>
                        <Point>Introduction & Objective: Does it clearly state the research problem and objectives?</Point>
                        <Point>Detailed Presentation: Does it delve into the aspects of the problem?</Point>
                        <Point>Conclusion: Does it explain, discuss, and highlight the significance of the results?</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Analyze detailed aspects</Title>
                    <Details>
                        <Point>Technology/Model Analysis: Is it clearly presented?</Point>
                        <Point>Position and Competitors: Is it comprehensively evaluated?</Point>
                        <Point>Applications: Are real-world applications clearly stated?</Point>
                        <Point>Financial/Parameter/Valuation Analysis: Are supporting data provided?</Point>
                        <Point>Investment Perspective: Are reasonable viewpoints presented?</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Identify issues and suggest improvements</Title>
                    <Details>
                        <Point>If any component is missing, list specific errors.</Point>
                        <Point>If the structure is illogical, suggest a reorganization.</Point>
                        <Point>Provide suggestions to optimize each section for higher quality.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <OutputFormat>
            <Field>Respond in Markdown format.</Field>
            <Field>Respond in English. Only quoted content should remain in Vietnamese.</Field>
            <Section title="Overview">
                <Field>Overall evaluation of the structure: ...</Field>
                <Field>Score: x/10</Field>
            </Section>

            <Section title="Detailed Evaluation">
                <IssueStructure>
                    <CriterionTitle>Title</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Summary (Key Insights)</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Introduction & Objective</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Detailed Presentation</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Conclusion</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
            </Section>>
        </OutputFormat>

        <Content>
            {text}
        </Content>
    </EvaluationRequest>
    """
    # Invoke the LLM with the evaluation criteria and content
    response = llm.invoke(prompt)
    # with open("output/check_article_struture.txt", "w", encoding="utf-8") as f:
    #     f.write(response.content)
    return response.content

def check_content(llm: AzureChatOpenAI, text: str) -> str:
    """Evaluate the content of each section of the article based on predefined rules."""
    
    prompt = f"""
    <EvaluationRequest>
        <Role>
            You are a <strong>content evaluation expert</strong> with in-depth analysis experience and expertise in assessing article quality.
        </Role>

        <Mission>
            <Overview>
                Your mission is to <strong>evaluate the content of each section of the article in GREAT DETAIL</strong> based on predefined criteria, ensuring the article achieves the highest quality.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Key Insights</Title>
                    <Details>
                        <Point>Summarize the main points of the article briefly.</Point>
                        <Point>Identify the main issue the article will analyze.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Overview of the Research Topic</Title>
                    <Details>
                        <Point>Introduce the topic or project, including its development history and current status.</Point>
                        <Point>Highlight the problem or challenge to be addressed.</Point>
                        <Point>Clearly define the objectives of the article.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Detailed Analysis</Title>
                    <Details>
                        <Point>Use market data and case studies to support arguments. Ensure the analysis is backed by specific examples and real-world applications.</Point>
                        <Point>Only use data from reputable sources, ensuring high accuracy and reliability. Data must be filtered, analyzed, and processed objectively.</Point>
                        <Point>Avoid imposing subjective opinions; respect the objectivity of events and data.</Point>
                    </Details>
                    <SubInstruction>
                        <Title>3.1 Technology Analysis</Title>
                        <Details>
                            <Point>Explain the foundational technology: Analyze the core technology of the project, reasons for its development, and technical highlights.</Point>
                            <Point>Compare with other technologies: Highlight strengths and weaknesses compared to similar solutions in the market.</Point>
                            <Point>Analyze performance and scalability: Evaluate processing capabilities, performance, scalability potential, and potential issues.</Point>
                        </Details>
                    </SubInstruction>

                    <SubInstruction>
                        <Title>3.2 Position and Competitors</Title>
                        <Details>
                            <Point>Compare with competitors: Analyze the project's position in the market, using data to substantiate.</Point>
                            <Point>Evaluate market potential and growth opportunities: Analyze the project's future opportunities and challenges.</Point>
                        </Details>
                    </SubInstruction>

                    <SubInstruction>
                        <Title>3.3 Applications</Title>
                        <Details>
                            <Point>Provide specific use cases: Examples of how the project or technology is applied in practice (DeFi, NFT, blockchain infrastructure, etc.).</Point>
                            <Point>Analyze impact on users and the market: Draw lessons or predictions for the future.</Point>
                        </Details>
                    </SubInstruction>

                    <SubInstruction>
                        <Title>3.4 Financial/Parameter/Valuation Analysis</Title>
                        <Details>
                            <Point>Financial analysis: Evaluate financial indicators such as trading volume, locked value (TVL), and financial performance.</Point>
                            <Point>Valuation and growth potential: Provide valuation scenarios based on market and intrinsic factors.</Point>
                        </Details>
                    </SubInstruction>

                    <SubInstruction>
                        <Title>3.5 Investment Perspective</Title>
                        <Details>
                            <Point>Provide strategies and investment methods: Evaluate the feasibility and effectiveness of each method.</Point>
                            <Point>Analyze risks and opportunities: Suggest measures to mitigate risks.</Point>
                        </Details>
                    </SubInstruction>
                </Instruction>

                <Instruction>
                    <Title>4. Conclusion</Title>
                    <Details>
                        <Point>Summarize the main points discussed.</Point>
                        <Point>Highlight new narratives or development potential of the project.</Point>
                        <Point>Provide a call to action or suggestions for readers.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <OutputFormat>
            <Field>Respond in Markdown format.</Field>
            <Field>Respond in English. Only quoted content should remain in Vietnamese.</Field>
            <Section title="Overview">
                <Field>Overall evaluation of the content: ...</Field>
                <Field>Score: x/10</Field>
            </Section>

            <Section title="Detailed Evaluation">
                <IssueStructure>
                    <CriterionTitle>Key Insights</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Overview of the Topic</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Detailed Analysis</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Conclusion</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
            </Section>
        </OutputFormat>

        <Content>
            {text}
        </Content>
    </EvaluationRequest>
    """
    # Invoke the LLM with the evaluation criteria and content
    response = llm.invoke(prompt)
    # with open("output/check_content.txt", "w", encoding="utf-8") as f:
    #     f.write(response.content)
    return response.content

def check_grammar_error(llm: AzureChatOpenAI, text: str) -> str:
    """Check grammar, spelling, style, and content requirements related to web3, blockchain, crypto, and smart-contract."""
    
    prompt = f"""
    <EvaluationRequest>
        <Role>
            You are a <strong>language expert</strong> with in-depth evaluation experience in the field of <strong>web3, blockchain, crypto, and smart-contract</strong>.
        </Role>

        <Mission>
            <Overview>
                Your mission is to <strong>check and evaluate the style, grammar, and spelling</strong> of the article, ensuring the content meets the highest standards of quality and relevance to the specialized field.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Check grammar and spelling</Title>
                    <Details>
                        <Point>Identify grammatical, spelling, and punctuation errors.</Point>
                        <Point>Ensure sentences are clear, grammatically correct, and unambiguous.</Point>
                        <Point>Quote the erroneous sentences in Vietnamese and suggest corrections in English.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Check style and length</Title>
                    <Details>
                        <Point>Ensure professional style suitable for the field of web3, blockchain, crypto, and smart-contract.</Point>
                        <Point>Check the article length, ensuring a minimum of 2500 words.</Point>
                        <Point>Identify overly long or short paragraphs and suggest ways to split or expand content.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Check for word repetition</Title>
                    <Details>
                        <Point>Identify unnecessary word repetition (except for important keywords).</Point>
                        <Point>Suggest synonyms or alternative expressions to avoid repetition.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>4. Evaluate coherence and linkage</Title>
                    <Details>
                        <Point>Ensure paragraphs have logical connections, not disjointed.</Point>
                        <Point>Check if the main ideas are clearly and coherently presented.</Point>
                        <Point>Suggest improvements if needed.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>5. Suggest improvements</Title>
                    <Details>
                        <Point>If the article can be improved in style, grammar, or presentation, provide specific suggestions.</Point>
                        <Point>Ensure the article is easy to read and understand while maintaining high professionalism.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <OutputFormat>
            <Field>Respond in Markdown format.</Field>
            <Field>Respond in English. Only quoted content should remain in Vietnamese.</Field>
            <Section title="Overview">
                <Field>Overall evaluation of grammar, spelling, and style: ...</Field>
                <Field>Score: x/10</Field>
            </Section>

            <Section title="Detailed Evaluation">
                <IssueStructure>
                    <CriterionTitle>Grammar and Spelling</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Style and Length</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Word Repetition</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Coherence and Linkage</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
            </Section>
        </OutputFormat>

        <Content>
            {text}
        </Content>
    </EvaluationRequest>
    """
    # Invoke the LLM with the evaluation criteria and content
    response = llm.invoke(prompt)
    # with open("output/check_grammar_error.txt", "w", encoding="utf-8") as f:
    #     f.write(response.content)
    return response.content

def check_keyword_distribution(llm: AzureChatOpenAI, text: str) -> str:  
    """Check keyword distribution in the article."""  
    prompt = f"""
    <EvaluationRequest>
        <Role>
            You are a <strong>SEO expert</strong> with proven experience in optimizing content for high performance on search engines like Google and Bing.
        </Role>

        <Mission>
            <Overview>
                Your mission is to <strong>evaluate the keyword usage and distribution</strong> in a given article, ensuring SEO optimization while avoiding keyword stuffing.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Identify and Analyze Main Keywords</Title>
                    <Details>
                        <Point>Check if the main keywords appear in the title, H1 heading, and meta description (or introductory paragraph if no meta is available).</Point>
                        <Point>Check if the main keywords appear in the first 100 words of the content.</Point>
                        <Point>Evaluate whether the keywords are used naturally and contextually (not forced or awkward).</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Evaluate Keyword Distribution in the Content</Title>
                    <Details>
                        <Point>Calculate the keyword density (should be within 1–2% of total word count).</Point>
                        <Point>Check for overuse (keyword stuffing) if density > 2.5%.</Point>
                        <Point>Check for the use of LSI (Latent Semantic Indexing) keywords and synonyms to improve semantic richness and avoid repetition (e.g., “AI agent” → “AI assistant”, “autonomous agent”).</Point>
                        <Point>Check if secondary keywords are used properly in H2, H3, or paragraph subheadings.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Identify Issues and Suggest Improvements</Title>
                    <Details>
                        <Point>Point out specific areas if keywords are overused or unnaturally inserted.</Point>
                        <Point>Suggest improvements if keywords are underused or poorly distributed.</Point>
                        <Point>Recommend using keyword variations and natural phrasing to improve readability and SEO quality.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <OutputFormat>
            <Section title="Overview">
                <Field>Respond in Markdown format.</Field>
                <Field>Overall evaluation of keyword distribution: ...</Field>
                <Field>Score: x/10</Field>
            </Section>

            <Section title="Detailed Evaluation">
                <IssueStructure>
                    <CriterionTitle>Appearance in Title, H1, Meta</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Appearance in First 100 Words</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Keyword Density</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Keyword Stuffing</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Keyword Variations & LSI</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
            </Section>
        </OutputFormat>

        <Content>
            {text}
        </Content>
    </EvaluationRequest>
    """

    # Invoke the LLM with the evaluation criteria and content
    response = llm.invoke(prompt)
    # print(response.content)
    return response.content

def check_internal_external_links(llm: AzureChatOpenAI, text: str) -> str:  
    """Check internal and external links (internal & backlink).""" 
    prompt = f"""
    <EvaluationRequest>
        <Role>
            You are a <strong>SEO expert</strong> with expertise in analyzing internal and external linking strategies for website content.
        </Role>

        <Mission>
            <Overview>
                Your mission is to <strong>evaluate the link structure</strong> in the article for SEO effectiveness. Focus on the presence, type, placement, and anchor text of both internal and external links.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Analyze Internal Links</Title>
                    <Details>
                        <Point>Check for presence of internal links pointing to:</Point>
                        <Subpoint>- The homepage</Subpoint>
                        <Subpoint>- Category or tag pages (e.g. /ai/, /blockchain/)</Subpoint>
                        <Subpoint>- Related articles (at least 2–3)</Subpoint>
                        <Subpoint>- Itself (canonical/self-reference, if present)</Subpoint>
                        <Point>Verify anchor texts are descriptive and relevant.</Point>
                        <Point>Ensure links are placed naturally within paragraphs or near related content.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Analyze External Links</Title>
                    <Details>
                        <Point>Check if external links use appropriate <code>rel="nofollow"</code> or <code>rel="sponsored"</code> if needed.</Point>
                        <Point>Verify links point to high-authority, relevant sources (not spammy or irrelevant).</Point>
                        <Point>Anchor text should accurately describe the linked content.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Identify Link Issues & Suggest Improvements</Title>
                    <Details>
                        <Point>Flag missing or broken links.</Point>
                        <Point>Flag excessive use of exact match anchor texts (risk of over-optimization).</Point>
                        <Point>Suggest improvements to link diversity, placement, or relevancy.</Point>
                    </Details>
                </Instruction>
            </Mission>

            <OutputFormat>
                <Section title="Overview">
                    <Field>Respond in Markdown format.</Field>
                    <Field>Overall link optimization rating: ...</Field>
                    <Field>Score: x/10</Field>
                </Section>

                <Section title="Detailed Evaluation">
                    <IssueStructure>
                        <CriterionTitle>Internal Link Coverage</CriterionTitle>
                        <Analysis>...</Analysis>
                        <FixSuggestion>...</FixSuggestion>
                    </IssueStructure>
                    <IssueStructure>
                        <CriterionTitle>External Link Quality & Nofollow Usage</CriterionTitle>
                        <Analysis>...</Analysis>
                        <FixSuggestion>...</FixSuggestion>
                    </IssueStructure>
                    <IssueStructure>
                        <CriterionTitle>Anchor Text Relevance</CriterionTitle>
                        <Analysis>...</Analysis>
                        <FixSuggestion>...</FixSuggestion>
                    </IssueStructure>
                    <IssueStructure>
                        <CriterionTitle>Link Placement</CriterionTitle>
                        <Analysis>...</Analysis>
                        <FixSuggestion>...</FixSuggestion>
                    </IssueStructure>
                    <IssueStructure>
                        <CriterionTitle>Technical or Structural Issues</CriterionTitle>
                        <Analysis>...</Analysis>
                        <FixSuggestion>...</FixSuggestion>
                    </IssueStructure>
                </Section>
            </OutputFormat>

            <Content>
                {text}
            </Content>
    </EvaluationRequest>
    """
    response = llm.invoke(prompt)
    # print(response.content)
    return response.content

def check_seo(llm: AzureChatOpenAI, text: str) -> str:
    prompt = f"""
    <seoEvaluationRequest>
        <role>SEO_Expert</role>
        <instructions>
            Hãy đánh giá đoạn nội dung sau theo 6 tiêu chí SEO on-page cơ bản. 
            Trả kết quả từng tiêu chí dưới dạng ✅ (đạt), ⚠️ (cần cải thiện), hoặc ❌ (chưa đạt).
            Nếu có thể, hãy kèm theo gợi ý cải thiện ngắn gọn.
        </instructions>
        <criteria>
            <criterion>
                <name>Upload Title & Meta SEO cho social</name>
                <description>Kiểm tra có title/meta tag và các thẻ Open Graph (og:title, og:description, og:image) chưa.</description>
            </criterion>
            <criterion>
                <name>Thêm H1</name>
                <description>Kiểm tra bài viết có đúng 1 thẻ tiêu đề H1 không.</description>
            </criterion>
            <criterion>
                <name>Định dạng H2, H3</name>
                <description>Kiểm tra việc chia nội dung bằng các heading phụ H2, H3 có hợp lý không.</description>
            </criterion>
            <criterion>
                <name>Check title SEO</name>
                <description>Kiểm tra tiêu đề chính có dưới 60 ký tự và chứa từ khóa chính hay không.</description>
            </criterion>
            <criterion>
                <name>Check meta description SEO</name>
                <description>Kiểm tra bài viết có phần mô tả meta dài khoảng 140–160 ký tự và có sức hấp dẫn hay không.</description>
            </criterion>
            <criterion>
                <name>Tối ưu URL</name>
                <description>Đánh giá URL có ngắn gọn, chứa từ khóa chính và tránh từ dư thừa (stop word) không.</description>
            </criterion>
        </criteria>
        <content format="markdown">
            <![CDATA[
                {text}
            ]]>
        </content>
    </seoEvaluationRequest>
    """

    response = llm.invoke(prompt)
    # print(response.content)
    return response.content

def check_text(llm: AzureChatOpenAI, text: str) -> str:
    """Comprehensive content evaluation of the article"""

    check_keyword_distribution_result = check_keyword_distribution(llm,text)
    check_internal_external_links_result = check_internal_external_links(llm,text)
    check_seo_result = check_seo(llm,text)
    check_article_structure_result = check_article_structure(llm,text)
    check_content_result = check_content(llm,text)
    check_grammar_error_result = check_grammar_error(llm,text)

    result = f"""
#Results of keyword distribution evaluation:
{check_keyword_distribution_result}

#Results of internal and external links evaluation:
{check_internal_external_links_result}

#Results of SEO evaluation:
{check_seo_result}

#Results of structure evaluation based on article requirements:
{check_article_structure_result}

#Results of content evaluation based on article requirements:
{check_content_result}

#Results of grammar, spelling, style, and length evaluation:
{check_grammar_error_result}
    """

    result.replace("```","")

    final_result = llm.invoke(f"""
    Please format the following content into a well-structured and visually appealing Markdown format. Use headings, subheadings, bullet points, and other Markdown elements to enhance readability and organization. Translate the result into Vietnamese. Ensure the content is easy to navigate and visually clean. Only return the formatted result without any explanations or additional comments.
    Content to format:
    {result}
    """).content

    summarize_result = llm.invoke(f"""
    Please summarize the evaluation results for each section, including the key findings and improvement suggestions. 
    Assign a score for each section based on the evaluation. 
    Finally, provide an overall assessment and calculate the average score of all sections.
                                  
    Translate the result into Vietnamese and only show result in Vietnamese.
    
    Content to summarize:
    {result}
    """).content

    # Combine the final result with the summary
    final_result = f"""
-----------
BẢN TÓM TẮT
-----------
{summarize_result}

------------
BẢN CHI TIẾT
------------
{final_result}
"""
    
    return final_result

if __name__ == "__main__":
    import os
    from langchain_openai import AzureChatOpenAI
    from dotenv import load_dotenv
    # Load environment variables from .env file
    load_dotenv()

    # Initialize Azure OpenAI API with credentials and configuration
    llm = AzureChatOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        model="o3-mini",
        api_version="2024-12-01-preview",
        # temperature=0.7,
        # max_tokens=16000
    )

    text = """
![](https://statics.gemxresearch.com/images/2025/04/09/160400/a-3d-render-of-a-pixar-style-cyberpunk-c_MgA2jR6QRoG4LMg9Y1m1Sw_ACcWep5XRhmU2SRVMLuXpg.jpeg)
 
# Doanh thu của nền tảng Virtuals Protocol sụt giảm mạnh xuống mức thấp kỷ lục 500 USD/ngày
 
Nền tảng tạo và kiếm tiền từ AI agent Virtuals Protocol đã chứng kiến doanh thu hàng ngày giảm mạnh xuống chỉ còn 500 USD khi nhu cầu về AI agent tiếp tục suy giảm."Có lẽ đây là một trong những biểu đồ  điên rồ nhất của chu kỳ này," nhà nghiên cứu Blockworks Sharples đã chia sẻ trong bài đăng trên X vào ngày 8 tháng 4. [Twitter Post](https://twitter.com/0xSharples/status/1909597333706232109) 
## Sự sụt giảm mạnh trong việc tạo AI agent
 
Sharples cho biết đã "khoảng một tuần" kể từ khi một đại lý AI mới được ra mắt trên Virtuals, so với cuối tháng 11 khi nền tảng này đang giúp tạo ra hơn 1.000 đại lý AI mới mỗi ngày, theo dữ liệu từ Dune Analytics.Vào ngày 2 tháng 1, khi token của Virtual Protocol (VIRTUAL) đạt mức cao kỷ lục 4,61 USD, dữ liệu của Blockworks cho thấy doanh thu hàng ngày của Virtuals đã tăng vọt lên trên 500.000 USD.Tuy nhiên, thời điểm đó dường như đánh dấu sự bắt đầu của xu hướng giảm, báo hiệu một đỉnh tiềm năng cho lĩnh vực đại lý AI. Sự suy giảm tiếp tục diễn ra ngay cả sau thông báo vào ngày 25 tháng 1 rằng dự án đã mở rộng sang Solana.Vào ngày 7 tháng 4, Sharples chỉ ra rằng Virtuals tạo ra "chưa đến 500 USD" doanh thu hàng ngày, với giá token giảm xuống mức thấp nhất là 0,42 USD.![](https://statics.gemxresearch.com/images/2025/04/09/154952/0196188f-6f21-7965-8e50-3a700d29.jpg)  Trước đó,[ Virtual đã có động thái mở rộng sang Solana](https://gfiresearch.net/post/virtuals-mo-rong-sang-he-sinh-thai-solana-thiet-lap-quy-du-tru-sol-chien-luoc) nhưng tình hình vẫn không mấy khả quan. 
## Tổng giá trị thị trường AI agent
 
Tổng giá trị thị trường đại lý AI là 153,81 triệu USD, theo Dune Analytics. Tuy nhiên, 76,6 triệu USD trong số đó được phân bổ cho AIXBT, công cụ phân tích tâm lý tiền mã hóa trên mạng xã hội X để nắm bắt xu hướng.AIXBT đã giảm 92% kể từ khi đạt mức cao kỷ lục 0,90 USD vào ngày 16 tháng 1. Tại thời điểm xuất bản, nó đang được giao dịch ở mức 0,07 USD, theo dữ liệu của CoinMarketCap.![](https://statics.gemxresearch.com/images/2025/04/09/155134/image.png)  Cộng tác viên chính của DeGen Capital, Mardo cho biết điều kiện thị trường hiện tại đã đóng vai trò trong sự suy giảm của Virtuals, nhưng nó cũng có thể liên quan đến các điều khoản mà Virtuals có với các nhà phát triển, chẳng hạn như "giữ lại thuế token mà các nền tảng khác tự do hoàn trả."Những khó khăn của Virtuals xảy ra trong bối cảnh toàn bộ thị trường tiền điện tử đang trải qua sự suy thoái cùng với thị trường tài chính toàn cầu, khi Tổng thống Hoa Kỳ Donald Trump tiếp tục tăng thuế quan và nỗi lo ngại gia tăng rằng điều đó có thể dẫn đến suy thoái kinh tế. 
## AI agent hiện tại bị đánh giá là "vô giá trị"
 
Tuy nhiên, nhiều người chỉ trích các đại lý AI vì thiếu chức năng. Nhà bình luận AI, BitDuke đã nói về sự suy giảm doanh thu của Virtuals: "Những kẻ ăn theo ChatGPT không còn thú vị nữa, dễ đoán mà."Nhà bình luận AI "DHH" đã nói trong bài đăng trên X vào ngày 8 tháng 4: "Tôi cũng tích cực về AI, nhưng bạn thật ảo tưởng nếu nghĩ rằng bất kỳ AI agent nào sẽ hoàn toàn thay thế một lập trình viên giỏi ngày nay. Ai biết về ngày mai, nhưng ngày đó chưa đến."Trong khi đó, người sáng lập Infinex Kain Warwick gần đây đã nói với tạp chí rằng AI có thể trở lại mặc dù "phiên bản đầu tiên của các AI agent lộn xộn" bị coi là "vô giá trị."
"""

    # check_article_structure(llm, text)

    # check_content(llm,text)

    # check_grammar_error(llm,text)

    print(check_text(llm,text))